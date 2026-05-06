# Drift Consultation Log — Foundation 2: Define
**Student:** Francis Kelechi Njoku
**Course:** CIDM 6330 — Software Architecture, Spring 2026
**Tool:** Drift Consultation CustomGPT (by Jeffry Babb)
**Session URL:** https://chatgpt.com/g/g-69dabde1bbec8191896617ab0afb625e-drift-consultation
**Date:** 2026-05-05
**Topic:** Scoped architectural assumptions in dry-run behavior, present-only persistence, and fail-fast API acquisition

---

## Full Consultation Transcript

---

**Student:**
Foundation 2 — Define.

In Foundation 1, my main gap was that I kept evaluating decisions based on what the technology gave me today, and only discovered the lifecycle consequences under probing. The feedback was to identify lifecycle and reversibility consequences before making decisions, so they become intentional rather than retrospective. I want to try to do that here from the start.

I built two things in Foundation 2: a FRED API consumer in kata-03 with exponential backoff retry logic, and a CSV-to-SQLite pipeline in kata-04 with validation, growth rate computation, and a --dry-run flag.

I used INSERT OR REPLACE again in kata-04 — same as kata-02. This time I am naming the consequence deliberately before you ask: that choice makes the system present-only again, no temporal memory, same closed doors as before. I accepted that because kata-04 is still a single-run batch pipeline and reproducibility was not a requirement I was building toward. That was a conscious trade this time, not an accidental one.

What I am genuinely less certain about is the --dry-run flag. I added it so I could inspect the pipeline without writing anything to disk. But I am not sure whether that partially reopens the reproducibility door or whether it solves a completely different problem. My instinct is that it solves "inspect without writing" — not "reconstruct a past state" — but I want that tested.

I also raised RuntimeError after retries are exhausted in kata-03 instead of returning an empty list. I had a reason at the time — an empty list is a valid result and I did not want silent failures. But I did not think about what that decision does when this function sits inside a larger multi-stage pipeline. Can you probe both?

---

**CustomGPT:**
Good. You're already showing improvement from Foundation 1 because you're naming consequences *before* being cornered into them.

You identified:
- present-only storage model
- intentional acceptance of lost temporal history
- distinction between inspection and reconstruction

That's movement.

Let's isolate one thread first.

You said: "My instinct is that --dry-run solves inspect-without-writing, not reconstruct-a-past-state."

I think that instinct is mostly correct — but I want you to pressure-test it structurally.

**Question:** What kind of architectural characteristic does --dry-run actually support? Not "what does it do mechanically." What property of the system becomes better because this mode exists? And be careful here: don't say "debuggability" unless you can explain for whom and at what stage of the system lifecycle.

---

**Student:**
The architectural characteristic --dry-run supports is safe pre-commit validation. The property that becomes better is operational confidence at the point of first execution.

Let me be specific about who and when.

The person who benefits is me, or anyone else running this pipeline against a new CSV file for the first time. At that stage, before a single row is written to the database, I cannot know whether the input is well-formed, whether the date column is named correctly, or whether the row count looks right. The --dry-run path lets me exercise the extract and validate stages of the pipeline — the parts that read and parse — without triggering the load, compute, and report stages that produce irreversible side effects.

What becomes architecturally better is that the boundary between "processing" and "committing" is now explicit and traversable. Before dry-run existed, there was only one mode: run the pipeline and find out what happened after the fact. With --dry-run, there are two modes — inspect and execute. That separation is a real structural property, not just a convenience flag.

What I want to be honest about is what it does not support. It does not improve reproducibility. It does not reopen the temporal memory door from Foundation 1. Once I commit a run, the same present-only, single-canonical-state issues remain. --dry-run only helps before the first write — it has no value for asking "what state was the system in last month?" That is a different problem, and this flag does not touch it.

So the precise answer is: --dry-run supports safe operability at the validation stage. It makes the pipeline safer to invoke for the first time against unknown input. It does not make the pipeline more reproducible, more auditable, or more temporally aware. I named those as separate concerns in Foundation 1, and this flag belongs in a different category from those.

---

**CustomGPT:**
Good distinction. You did **not** overclaim --dry-run, and you located it in the pipeline lifecycle: before commit, not after history has changed.

Now I want to test the phrase you used: "the boundary between processing and committing is now explicit." That sounds architectural, but it may be thinner than you think.

**Question:** In your implementation, is --dry-run a true structural separation between validation and commit, or is it just a conditional branch that skips writing? What would I see in the code that proves one versus the other?

---

**Student:**
Honestly, it is a conditional branch, not a true structural separation. And I can show that directly from the code.

In run_pipeline, the dry_run flag is a boolean parameter. The function starts by calling extract_rows regardless of mode. Then there is a single if dry_run: block that calls validate_and_transform with log_path=None and prints a summary, then returns early. The non-dry-run path falls through to init_db, load_rows, compute_growth_rates, and generate_report.

What you would see in the code that proves it is a branch rather than a structure is this: there is one function, one entry point, and the separation exists only because a boolean check skips the write half. Nothing in the type system or function signatures enforces the boundary. If I called load_rows directly, there is nothing structural stopping that in dry-run mode. The boundary is a convention held together by an if statement, not by the shape of the code.

A true structural separation would look different. There would be a validate_pipeline function that returns a result — something like a list of validated rows and a summary — and a separate execute_pipeline function that takes that result and commits it. The two stages would be callable independently. You could call validate_pipeline, inspect what it returns, and only then decide whether to pass the result to execute_pipeline. The boundary would be enforced by the interface, not by a flag.

What I actually built is closer to a --dry-run flag on a CLI tool than an architectural separation between validation and commitment. It is useful for the reason I said earlier — safe pre-commit inspection — but I overclaimed when I said the boundary was explicit in a structural sense. The boundary is explicit to the developer reading the code. It is not enforced by the system itself.

That is a real distinction, and I did not see it until now.

---

**CustomGPT:**
Good. That correction matters.

You found the difference between:
- **behavioral option**: "skip writes when this flag is set"
- **structural boundary**: "validation and commit are separate responsibilities with separate interfaces"

That is Foundation 2 territory: not just what the code does, but how responsibilities are arranged.

Now let's connect it to the larger pipeline.

**Question:** What risk does the current boolean-branch version introduce if this pipeline grows? Not "it is less clean." What specific future mistake becomes easier because validation and commit are not structurally separated?

---

**Student:**
The specific mistake that becomes easier is this: the two branches silently diverge, and the dry-run stops telling the truth.

Here is the concrete version of that risk in my actual pipeline.

Right now, validate_and_transform is called in both branches — but with different arguments. In the dry-run branch, it is called with log_path=None. In the real branch, it is called with the actual log path. They are the same function, but already receiving different inputs. The two paths are not identical — they just happen to produce similar enough output that no one has noticed yet.

If the pipeline grows and I add a new validation step — say, a check that rejects GDP values below a plausible floor — I have to remember to apply it in both branches. There is nothing in the code that reminds me to do that. If I add it only to the real path, the dry-run will pass validation on data that the real run would reject. I now have a false confidence problem: dry-run says the input is clean, I commit, the real run fails.

That is worse than not having a dry run at all, because it looks like I checked.

The same risk applies in reverse. If I add a pre-processing step to the dry-run branch as a debugging aid and forget to remove it, the dry-run is now testing something the real run does not do. The two paths have drifted and I have no structural signal telling me that happened.

With a true structural separation — a validate_pipeline function that both branches call in exactly the same way — the divergence cannot happen silently. If validate_pipeline changes, both paths change because they share the same interface. The current boolean branch has no such guarantee. It relies on the developer remembering to keep both branches consistent, and that is the kind of assumption that breaks as a pipeline grows and different people touch it at different times.

---

**CustomGPT:**
Good. That is the right risk: **validation drift**.

You also named the real architectural concern: dry-run can become a *false assurance mechanism* if it does not exercise the same validation path as execution.

Now we move to kata-03.

You said: "I raised RuntimeError after retries are exhausted instead of returning an empty list."

**Question:** In a larger multi-stage pipeline, what does raising RuntimeError optimize for, and what does it sacrifice? Don't answer as Python mechanics. Answer as pipeline behavior.

---

**Student:**
Raising RuntimeError optimises for correctness at the cost of resilience.

In pipeline terms, what that means is this: the pipeline fails loudly and completely the moment acquisition fails. No downstream stage runs on bad data. The load stage never sees zero rows and writes an empty database. The report stage never produces a summary that says "0 observations" and looks like a successful run. The failure is unmistakable, and it stops propagation immediately. That is what it is optimising for — a guarantee that if the acquisition did not succeed, nothing downstream will silently pretend it did.

What it sacrifices is resilience and composability.

In my current pipeline, acquisition is the only stage that talks to an external system, so a single exception stops one thing. But in a larger pipeline with multiple acquisition sources — say, fetching GDP, CPI, and unemployment data in sequence — a RuntimeError on the first source aborts the entire pipeline. The two sources that would have succeeded never ran. There is no partial result, no indication of what would have worked, just a crashed process. The pipeline has no way to say, "I got two of three series, here is what I have."

The second cost is that RuntimeError spreads exception-handling responsibility to every caller. Anything that calls this function now needs a try/except block or the exception propagates all the way up and kills the process. In a single-stage pipeline that is manageable. As the pipeline grows and this function gets called from more places, that exception-handling obligation multiplies. The callers start making decisions about failure that should belong to the acquisition stage itself.

I made this decision for the right reason — I did not want silent failures masquerading as empty results. But I made it without thinking about what it does to a pipeline that grows beyond one acquisition source. That is the same pattern as Foundation 1: I optimised for one property, correctness, without naming what I was giving up in terms of resilience and composability. The deliberate version of this decision would have said: "I am choosing fail-fast because I only have one acquisition source and a partial result is worse than no result for this pipeline." I did not say that at the time.

---

**CustomGPT:**
Good. You named the trade cleanly: **fail-fast correctness** over **partial resilience**.

Now I want to challenge one phrase: "The callers start making decisions about failure that should belong to the acquisition stage itself." Maybe. But maybe not.

**Question:** Who *should* own the decision about whether partial data is acceptable: the FRED API consumer, or the larger pipeline orchestration layer? Answer for your actual context first, then say how that changes if GDP, CPI, and unemployment become separate sources.

---

**Student:**
For my actual context, the acquisition stage should own the decision — and RuntimeError is the right call.

In kata-03, there is one source, one series, one acquisition call. The pipeline either has GDP data or it has nothing. There is no partial result to reason about. If the FRED request fails after five retries, there is nothing downstream worth running — the report would be empty, the growth rates would be uncalculated, and the whole run would be meaningless. In that context, the acquisition function raising RuntimeError is not overstepping. It is correctly saying: I failed, there is nothing here, stop. The pipeline does not need to make a decision because there is no decision to make.

That changes completely if GDP, CPI, and unemployment become separate sources.

Once there are multiple sources, "partial data" is a real concept, and the acquisition stage is the wrong place to decide whether it is acceptable. The GDP consumer does not know whether the pipeline can produce a meaningful report without CPI. That depends on what the report is trying to show, what downstream stages require, and what the caller considers a valid run. Those are orchestration-level concerns, not acquisition-level concerns.

In that context, the right responsibility split is: each acquisition function surfaces its failure cleanly — either by raising or by returning a typed result that signals success or failure — and the orchestration layer decides what to do with the combination. The orchestration layer is the only place with enough context to say "two of three sources succeeded, that is enough to proceed", or "CPI is required for this report, abort."

What I said earlier — that callers start making decisions that should belong to the acquisition stage — was wrong for the multi-source case. The acquisition stage should not own the partial-data decision because it does not have the context to make it. What I should have said is that RuntimeError is correct for a single-source pipeline, and the design needs to change — not the exception, but where the exception is caught and what the catcher is allowed to do with it, when the pipeline grows to multiple sources.

That is a lifecycle and reversibility consequence I did not think about when I wrote kata-03. The current design is right for the current scope. It becomes wrong the moment a second acquisition source is added, and the code gives no signal that that threshold exists.

---

**CustomGPT:**
Good correction. You separated **failure signaling** from **failure policy**.

For one source, they can live together. For multiple sources, they should separate:
- acquisition reports what happened
- orchestration decides whether the run is still valid

Now the Drift pressure point.

**Question:** What is the architectural threshold where your current kata-03 design stops fitting? Name the exact change in context that would force you to revisit RuntimeError handling — not vaguely "when it gets bigger."

---

**Student:**
The exact threshold is the second call to fetch_all_observations inside the same pipeline run.

That is the precise line. Not "when the pipeline gets bigger," not "when we add more data sources." The moment run_pipeline contains two sequential calls to fetch_all_observations for different series, GDP and CPI, for example, the current design breaks structurally.

Here is why that specific line is the threshold.

Right now, run_pipeline calls fetch_all_observations once. If that call raises RuntimeError, there is nothing else to attempt. The exception is correct because there is no second acquisition that could still succeed.

The moment a second call exists, this code:

    gdp_rows = fetch_all_observations(api_key, "GDP")
    cpi_rows = fetch_all_observations(api_key, "CPI")

becomes a problem. If the GDP call raises RuntimeError, the CPI call never runs. The orchestrator has no information about whether CPI would have succeeded. It cannot decide "I have CPI, can I produce a partial report?" because it never got the chance to ask. The exception from the first call consumed the entire pipeline's fate.

That is the architectural threshold: one acquisition call means failure is total and RuntimeError is appropriate. Two acquisition calls mean partial success is possible, and the orchestrator needs to be able to attempt both before deciding what to do with the combination.

What that means for the current code is that kata-03 is one design decision away from the threshold but not past it yet. The current pipeline fetches one series. As long as it stays in one series, RuntimeError is the right call, and nothing needs to change. The design becomes wrong at exactly the moment a second fetch_all_observations call is added to run_pipeline; not before, not vaguely later.

That threshold is invisible in the current code. Nothing in the function signature, the docstring, or the pipeline structure signals. This design assumes exactly one acquisition source. That is the real gap; not that the design is wrong today, but that it does not document the assumption it depends on.

---

**CustomGPT:**
Good. That is specific enough to be useful.

You named the hidden governing assumption: *This acquisition design assumes exactly one required source.*

Now shift from structure to governance.

**Question:** Where should that assumption live so future-you does not accidentally cross the threshold without noticing? Not what code would you write — where should the decision be visible?

---

**Student:**
The assumption should live in two places, and they serve different audiences.

The first is the ADR: the Architecture Decision Record. That is where the decision belongs at the level of intent. The ADR would record that the pipeline uses RuntimeError as its failure signal, that this design assumes exactly one required acquisition source, and critically, that this decision must be revisited the moment a second source is added. An ADR captures the why, the threshold, and the consequence; not just what was decided, but under what conditions it stops being valid. That is the document future-me reads before adding a second fetch call, not after the pipeline breaks.

The second is the call site in run_pipeline; the exact line where fetch_all_observations is called. Not a docstring on the function itself, because the acquisition function does not know it is the only source. That is a pipeline-level fact. A short inline note at the call site saying "single source assumed here; RuntimeError propagates to pipeline level; revisit if a second source is added" makes the assumption visible to anyone touching the orchestration layer. They do not need to read the ADR first. The warning is at the threshold.

Those two places serve different purposes. The ADR records the reasoning for someone making architectural decisions. The call site note warns the developer of implementation changes. Both are needed because the person adding a second acquisition source might not be the same person who wrote the original design, and might not think to look for an ADR before writing two lines of code.

What I did not do in Foundation 2 is write either of those things. The assumption exists in the code invisibly. Nothing surfaces until the pipeline breaks. That is the same pattern as Foundation 1; I made the right decision for the current scope, but I did not document the conditions under which it stops being right. The assumption became a silent constraint rather than a visible one.

---

**CustomGPT:**
Good. You've covered the governance dimension now.

You distinguished:
- **ADR** = decision intent, scope, revisit threshold
- **call-site note** = implementation warning at the point of risk

That is the right split.

One more probe before closing.

**Question:** Across --dry-run, INSERT OR REPLACE, and RuntimeError, what is the repeated pattern in your Foundation 2 decisions? Name the pattern as a weakness in your architectural thinking — not as a list of features.

---

**Student:**
The repeated pattern is this: I made decisions that are correct within an assumed scope, but I never named the scope.

INSERT OR REPLACE is correct if the pipeline runs once and reproducibility is not required. --dry-run is correct if both branches exercise the same validation logic. RuntimeError is correct if there is exactly one acquisition source. All three decisions work today. But in every case, the condition that makes them work is invisible. It exists as an assumption I was carrying silently, not as a constraint I stated explicitly.

That is the weakness. Not that I chose the wrong tools or reasoned poorly about the immediate problem. The weakness is that I treated each decision as a present-tense implementation choice rather than a scoped architectural commitment. I asked "does this work?" and stopped there. I did not ask "under what conditions does this stop working, and where does that condition live?"

The result is a codebase where the decisions are defensible but the thresholds are invisible. Anyone who adds a second acquisition source, extends the dry-run path, or introduces longitudinal reporting will cross one of those thresholds without knowing it exists. The code gives no signal. There is no ADR recording the assumption, no call-site note marking the threshold, no docstring stating the scope.

Foundation 1 named this as evaluating technology at the feature level instead of the lifecycle level. Foundation 2 repeated the same pattern at a different layer. I moved from "what does SQLite give me?" to "what does RuntimeError give me?" and still did not ask "what does this system need to stay true for this decision to remain valid?"

The habit I am missing is not reasoning about trade-offs — I can do that under probing. The habit I am missing is reaching for governance before reaching for implementation. Writing the assumption down before writing the code, so the threshold is visible from the start rather than reconstructed after the fact.

---

## Drift Consultation Summary

**Foundation:** 2
**Date:** 2026-05-05
**Topic:** Scoped architectural assumptions in dry-run behavior, present-only persistence, and fail-fast API acquisition

### Demonstrated Strengths

You clearly distinguished behavior from structure when you recognized that `--dry-run` was a conditional branch, not a true validation/commit boundary. You also named the exact threshold where `RuntimeError` stops fitting: the second acquisition source inside the same pipeline run.

### Areas Needing Development

Your decisions are often reasonable for the current scope, but the scope remains implicit. Across `INSERT OR REPLACE`, `--dry-run`, and `RuntimeError`, the weakness was not poor choice-making; it was failing to document the conditions under which each choice stops being valid.

### Unanswered Questions

- When should reproducibility become a driving characteristic instead of an accepted omission?
- What form of validation/commit separation is justified before the pipeline grows?
- How should multi-source acquisition report partial success without overengineering the current design?

### AI Collaboration Assessment

Your reasoning appears to be evolving. You corrected overclaims, separated failure signaling from failure policy, and identified invisible assumptions rather than defending the artifact.

### Signals Observed

- **Strong signal recognition** appeared when you identified hidden assumptions behind each feature.
- **Trade-off awareness** appeared in your fail-fast correctness versus partial resilience analysis.
- **Structural judgment** appeared when you distinguished a CLI flag from a real interface boundary.
- **Governance intent** appeared when you named ADRs and call-site notes as places where thresholds should live.

### Commitments for Next Foundation

Before implementing a decision, state the assumption that makes it valid, the threshold where it stops fitting, and where that threshold will be visible.

**Dimensions Covered:** Signal Recognition, Trade-Off Awareness, Structural Judgment, Governance & Intent
**Estimated Depth:** solid

---

## Drift Session Evaluation

**Foundation:** 2
**Date:** 2026-05-05

| Dimension | Score (1–4) | Points | Evidence |
|---|---|---|---|
| Signal Recognition | 4 | 19/20 | You identified that all three decisions were correct only under unstated scope assumptions. |
| Trade-Off Reasoning | 4 | 23/25 | You explained fail-fast correctness versus resilience and dry-run safety versus false assurance. |
| Structural Judgment | 3 | 17/20 | You distinguished conditional branching from structural separation, but only after probing. |
| AI Collaboration | 3 | 17/20 | You revised claims under pressure and showed evolving judgment rather than static justification. |
| Engagement Quality | 4 | 15/15 | You answered directly, acknowledged gaps, and named your recurring weakness clearly. |

**Total: 91/100**
**Estimated Depth:** solid
**Growth Trajectory:** accelerating

**Priority for Next Foundation:**
Make architectural thresholds visible before implementation: every major decision should include the scope assumption that makes it valid and the exact change that would force reconsideration.
