# Drift Consultation Log — Foundation 3: Develop
**Student:** Francis Kelechi Njoku
**Course:** CIDM 6330 — Software Architecture, Spring 2026
**Tool:** Drift Consultation CustomGPT (by Jeffry Babb)
**Session URL:** https://chatgpt.com/g/g-69dabde1bbec8191896617ab0afb625e-drift-consultation
**Date:** 2026-05-07
**Topic:** Concurrency trade-offs, stage boundary visibility, provenance handling, and governance constraints in a GDP data pipeline

---

## Full Consultation Transcript

---

**Student:**
Foundation 3 — Develop.

My Foundation 2 commitment was to name the scope assumption and the invalidation threshold for every architectural decision before being probed. I want to test whether I actually did that, not just whether I learned to say it.

Foundation 3 covered three things: kata-05 used ThreadPoolExecutor and an asyncio alternative with a semaphore to fetch URLs concurrently; kata-06 used ProcessPoolExecutor for CPU-bound statistics computation across chunked number ranges; and the GDP pipeline introduced a full acquire, transform, and report structure with a sample-data fallback when the FRED API is unavailable.

I will name the decisions and their assumptions upfront.

In kata-05, I chose ThreadPoolExecutor for the I/O-bound fetch loop on the basis that threads can overlap on network wait even though the GIL serialises CPU work. The scope assumption is that thread-creation overhead stays below per-request wait time — which holds for a small URL set but breaks down at scale. I built the asyncio alternative with a semaphore specifically because asyncio scales better when that assumption stops holding. I did not measure the crossover point.

In kata-06, I used ProcessPoolExecutor to bypass the GIL for CPU-bound prime counting. The scope assumption is that pickle serialisation cost for the chunk data is small relative to computation time. I accepted that trade without measuring it, which means I named the right executor but not the threshold where the trade stops being favourable.

In the GDP pipeline, I kept raw JSON and transformed JSON in separate directories. The assumption is that transformations may need to be re-run against original data without re-fetching from the API. The threshold — where storage duplication costs more than recovery ability is worth — is nowhere near for this dataset size, but I am naming it rather than leaving it invisible.

What I have not resolved is whether the acquire-to-transform-to-report structure is true stage separation or sequential function calls with no enforced boundary. That is the same question as --dry-run in Foundation 2, moved one level up. I suspect it is the latter, and I want that tested.

---

**CustomGPT:**
Good. You're doing something different now:

You're not just naming the trade-off. You're naming:

- the governing assumption
- the invalidation threshold
- the unmeasured variable

That's progress from Foundation 2.

Now let's pressure-test the pipeline structure question.

You said: "I suspect acquire → transform → report is sequential calls, not true stage separation."

Don't answer abstractly.

**Question:** What would I see in your code that proves these are merely sequential function calls instead of independently meaningful pipeline stages?

---

**Student:**
Honestly, what you would see is that none of the stages passes anything to the next one. `acquire()` writes a raw JSON file to disk. `transform()` does not receive that file from `acquire()` — it constructs the path from a config value and reads it directly. `report()` does the same with the transformed file. Each stage knows where to look; nothing is handed across.

That is what makes them sequential calls rather than separated stages. The coupling is real, but it is hidden inside the functions. Nothing in the signatures enforces the contract. If the raw file is missing, `transform()` fails at the file read, not at the boundary where it was supposed to receive input.

The one genuine improvement I made is keeping raw and transformed directories separate. That means I can re-run `transform()` against a previous acquisition without fetching again. That is real separation at the data level. But it is not the same thing as structural separation. The stages share a file-system convention, not an interface.

The threshold where this breaks is the same as --dry-run in Foundation 2: the moment I need to test one stage in isolation with injected data, or run stages in a different order, the current structure resists it. Today, it works because the only path is the full linear run. That assumption is invisible in the code.

---

**CustomGPT:**
Good. You found the key distinction:

**Data separation exists. Interface separation does not.**

That is not failure; it is a useful diagnosis. Your structure supports rerunning stages by filesystem convention, but not by explicit contracts.

Now test the architectural cost.

**Question:** What future change becomes harder because each stage discovers its own input path instead of receiving an explicit input artifact from the previous stage?

---

**Student:**
The change that becomes hardest is testing any single stage in isolation without the full pipeline running before it.

Right now, if I want to test that `transform()` correctly handles a malformed raw file, I have to create an actual file in the `raw/` directory first. I cannot pass in a Python object and say, "process this." The function constructs its own input path from the config and reads from disk. That means my test has to manage the file system; create the file, run the function, check the output file, and clean up. The test is no longer about `transform()`. It is also about file creation and path resolution.

That is a cost I will feel directly in Foundation 4 when I apply TDD to the analysis module. The habit there is: write a test with known input, run the function, and assert the output. If the function discovers its own input from the file system, that habit breaks. I have to choose between touching the file system in every test or refactoring the function before I can test it cleanly. Neither is free.

The second cost is the one that connects back to Foundation 2. The unanswered question there was how a multi-source pipeline reports partial success. In the current structure, if I add a CPI series alongside GDP, `acquire()` would write two files — say, `raw/gdp.json` and `raw/cpi.json`. But `transform()` has no way to receive both as inputs and decide whether both are required or one is sufficient for the pipeline to proceed. It reads one path. The decision about whether the pipeline has enough data to continue cannot live at the stage boundary because there is no stage boundary — there is only a file path. The orchestration logic would have to live somewhere else, probably inside `transform()` itself, which is the wrong place for it.

Both costs have the same root: when a stage discovers its own input, it cannot be told what input to use. It cannot be injected with a different artifact, a cached version, a test fixture, or a partial result. The function owns the decision about where its data comes from, and that makes it harder to control from the outside.

The threshold where this stops being acceptable is exactly what I named before: the second data source, or the first time I need to test a stage without running the pipeline from scratch.

---

**CustomGPT:**
Good. You named the cost without exaggerating it.

The repeated issue is **control from outside the stage**. Right now, the stage owns too much:

- where input comes from
- what artifact is valid
- whether the filesystem convention has been satisfied

That weakens testability and orchestration.

**Question:** If you refactored only one thing — without redesigning the whole pipeline — which stage boundary should become explicit first: acquire → transform, or transform → report?

Choose one, and justify it by architectural pressure, not convenience.

---

**Student:**
The `acquire → transform` boundary should become explicit first.

Not because it is easier to refactor, but because it is where the most architectural pressure is already concentrated.

Here is why that boundary carries more weight than the other one.

`acquire()` is the only stage that talks to an external system. It is also the stage with a fallback — when the FRED API is unavailable, it returns sample data instead of live data. Right now, `transform()` has no way of knowing which one it received. It reads a file, processes it, and writes another file. The information about data provenance — whether this is a live fetch or a fallback — is lost the moment `acquire()` writes to disk. If I made the boundary explicit and `acquire()` returned a result object that included a provenance flag alongside the raw observations, `transform()` could receive that and either act on it or pass it downstream. Right now it cannot, because there is no artifact crossing the boundary — only a file on disk.

The second pressure point is the Foundation 2 question that was never resolved: how does a multi-source pipeline report partial success? That question lives at exactly this boundary. If I add CPI alongside GDP, the orchestrator needs to know whether both acquisitions succeeded before deciding whether to run `transform()`. It cannot make that decision if `acquire()` just writes a file and returns nothing. The boundary has to become explicit before the orchestrator can reason about what it received.

The `transform → report` boundary has less pressure right now. Both stages deal with data that has already been acquired and validated. `report()` failing because the transformed file is missing is a problem, but it is downstream of the real risk. Fixing the `acquire → transform` boundary first also makes the `transform → report` boundary easier to address later — once data flows as explicit artifacts, the pattern applies consistently.

What this refactor does not fix is the `transform → report` coupling or the file-system convention altogether. I am not claiming one change solves the pipeline. I am saying that if only one boundary becomes explicit, it should be the one closest to the external system and the one where orchestration decisions need to be made.

---

**CustomGPT:**
Good. You chose based on pressure, not convenience.

You identified the real missing signal: **provenance**. If fallback sample data and live FRED data look identical after acquisition, the downstream system cannot reason honestly about what it is processing.

**Question:** If `acquire()` returns an explicit artifact, what is the minimum information that artifact must carry so `transform()` and the orchestrator can make better decisions?

Do not design a full class. Name the fields that matter and why.

---

**Student:**
Three fields. Not more than that for the decisions that actually need to be made.

`data` — the raw observations themselves. This is obvious, but naming it matters because right now, it is the only thing the pipeline implicitly transfers through the file. Everything else is lost.

`source` — a string marking whether this came from the live FRED API or the sample fallback. This is the provenance field the pipeline is currently missing. `transform()` does not need to behave differently based on it — the transformation logic is the same either way — but the orchestrator does. If the `source` is `"sample"`, a production run should log a warning or refuse to proceed, depending on configuration. Right now, that decision cannot be made because nothing downstream knows which source produced the data. The information disappears at the file write.

`series_id` — which series this artifact represents. For the current single-source pipeline, this feels redundant, but it is the field that makes multi-source orchestration possible without redesigning the artifact. If the orchestrator receives two artifacts — one for GDP, one for CPI — it can check both `series_id` values and decide whether it has everything it needs before calling `transform()`. Without it, the orchestrator has no way to reason about a collection of results. It just has anonymous blobs of data.

What I am deliberately leaving out is a timestamp or a fetch duration. Those are useful for observability and logging, but they do not change any decision `transform()` or the orchestrator makes about whether to continue or what to do with the data. Adding them now would solve a problem I do not have yet.

The scope assumption behind these three fields is that the pipeline is still single-series with one optional fallback. The threshold where this stops being enough is a pipeline that fetches multiple series with different fallback policies for each — at that point, the `source` becomes a richer status object, not a two-value string. But that threshold is not the current design, and I am not building toward a hypothetical.

---

**CustomGPT:**
Good restraint. You avoided turning the artifact into a logging envelope.

Now the pressure point:

You said: "`transform()` does not need to behave differently based on `source`; the orchestrator does."

That implies `transform()` should receive only what it needs, while the orchestrator sees the whole acquisition artifact.

**Question:** Where should the provenance decision live if sample fallback data appears during a run: before transform, after transform, or at report generation?

Choose one, and justify the timing.

---

**Student:**
Before the transformation. That is where the decision has the most leverage, and leverage is the right criterion here.

Here is why timing matters. Once `transform()` runs, the pipeline has committed to producing a result. The transformed file exists. The report stage will find valid input. At that point, flagging the provenance is disclosure — telling the user what happened — not a decision about whether to proceed. Those are different things, and conflating them is what makes the fallback dangerous in my current pipeline.

In my actual code, the `FRED_FALLBACK_TO_SAMPLE_ON_ERROR` flag already represents an orchestration-level policy: the caller decided in advance whether fallback is acceptable. What the pipeline does not currently do is check that decision against what actually happened before continuing. `acquire()` falls back silently, writes the sample file, and `transform()` processes it without knowing. The config flag exists, but the enforcement point does not.

The right enforcement point is the orchestrator, after receiving the acquisition artifact and before calling `transform()`. If the `source` is `"sample"` and the config says fallback is allowed, the orchestrator logs a warning and continues. If fallback is not allowed, it stops there — no transformation work is done on data that the pipeline was not supposed to use. Either way, the decision is made at the boundary with the most leverage and the least wasted work.

The place provenance should be surfaced to the user is the report — a visible label saying this output was generated from sample data. But surfacing and deciding are separate responsibilities. The report should disclose; the orchestrator should decide. Mixing them would mean the pipeline does all the work and then tells the user at the end that it probably should not have run. That is the same false-assurance problem as --dry-run in Foundation 2 — the check happens too late to be meaningful.

The scope assumption behind this is that the orchestrator exists as a distinct layer that receives artifacts and makes continuation decisions. In my current pipeline, it does not — `run_pipeline()` calls the stages sequentially without inspecting what they return. The decision about where provenance lives only becomes enforceable once the acquisition artifact is explicit. That is why the two changes are connected.

---

**CustomGPT:**
Good. You separated:

- **decision point**: orchestrator, before transform
- **disclosure point**: report, after transform

That is stronger Foundation 3 reasoning. You're thinking in terms of where control belongs, not just where data happens to be available.

**Question:** What risk did the sample-data fallback introduce that plain `RuntimeError` did not? Use your earlier Foundation 2 fail-fast reasoning as the contrast.

---

**Student:**
`RuntimeError` fails loudly and produces nothing. The sample-data fallback succeeds silently and produces something that looks real.

That is the specific risk the fallback introduces that `RuntimeError` did not.

In Foundation 2, I said that `RuntimeError` optimises for correctness at the cost of resilience — the pipeline stops the moment acquisition fails, no downstream stage runs on bad data, and the failure is unmistakable. The cost was that a single failed source aborts everything. But the failure is visible. Nobody looks at a crashed pipeline and draws conclusions from the output, because there is no output.

The fallback inverts that trade. The pipeline continues. Transform runs. Report runs. A complete GDP report is written to disk. It looks identical to a successful live run. The user who does not know about the fallback has no signal that anything went wrong. They have a report with hardcoded 2020 sample values and no indication that the FRED API was unavailable. That is not a recoverable failure — it is a plausible-looking artefact produced from the wrong input.

That is the false-assurance problem from Foundation 2 applied one level up. In Foundation 2, it was a dry run: if both branches do not exercise the same validation path, the dry run tells you the input is clean when the real run would reject it. Here is the full pipeline: if provenance does not flow through to the report, the pipeline tells the user the data is current when it is not.

`RuntimeError` never had this risk because it never produced an artefact. The fallback creates the risk precisely because it succeeds — it produces an output that has the same shape and format as a correct run, with no structural signal distinguishing it from one.

The assumption the fallback depends on is that the user will check the logs or the config before acting on the report. That is the same invisible scope assumption as Foundation 2 — the design is safe within that assumption, but the assumption is not stated anywhere near the output. The threshold where the fallback becomes actively dangerous is the first time a user reads the report without knowing the fallback activated.

---

**CustomGPT:**
Good. You named the risk precisely:

**A fallback converts visible failure into plausible false output.**

That is more dangerous than a crash when the artifact can be mistaken for truth.

**Question:** If fallback remains, what rule should govern it?

Not implementation. State the architectural rule that keeps fallback from becoming false assurance.

---

**Student:**
The rule is: a fallback run may not produce an artifact that is indistinguishable from a live run.

That is the complete rule. Everything else follows from it.

What it governs is not whether the fallback activates — that is a configuration decision, and the `FRED_FALLBACK_TO_SAMPLE_ON_ERROR` flag already handles it. What it governs is what the fallback is allowed to produce. If the pipeline falls back to sample data, the report it generates must carry a signal that it was not produced from the intended source. Not in the logs. Not in the config. In the artifact itself — the output the user reads.

The reason the rule has to be stated at the artifact level is what I identified in the previous answer: logs and configuration exist outside the output. A user reading the report does not see the logs. They see the report. If the report looks identical to a live-data run, the fallback has become false assurance regardless of what the logs say. The signal has to be where the conclusion is drawn.

This connects directly to the Foundation 2 pattern. In Foundation 2, the architectural rule was: a decision that is valid only within a scope must make that scope visible at the point where the decision matters. Here, the scope is "this output was produced from sample data." The point where it matters is the report — the artifact the user acts on. Burying the scope in a log entry or a config flag is the same invisible assumption I kept making in Foundation 2, just in a different part of the pipeline.

The rule does not say the fallback is wrong. It says the fallback is only acceptable if it cannot be mistaken for the truth. That is the governing constraint.

---

**CustomGPT:**
Good. That is a governance rule, not a patch.

You've now connected provenance to artifact trust.

**Question:** Across concurrency, CPU parallelism, stage boundaries, and fallback behavior, what is the repeated Foundation 3 pattern in your reasoning?

Name the weakness, not the features.

---

**Student:**
The repeated pattern is this: I built the structure but left the governing constraint implicit.

In Foundation 2, the weakness was that I made decisions correctly within an assumed scope, but never named the scope. Foundation 3 repeated the same habit at a different layer. I did not just leave scope assumptions invisible — I left the constraints that make each structure safe to use invisible as well.

In kata-05, I chose threading for I/O-bound work and built an asyncio alternative with a semaphore. The reasoning was correct. But the threshold — the point where thread-creation overhead exceeds per-request wait time — was never measured. I named the right executor without naming the condition under which it stays the right executor.

In kata-06, I chose ProcessPoolExecutor to bypass the GIL for CPU-bound work. Again, correct. But the pickle serialisation cost versus computation time tradeoff was stated qualitatively and left unmeasured. The constraint governing when that trade is favourable exists, but not in the code.

In the pipeline, I kept raw and transformed directories separate, which is genuine data-level separation. But the stage interfaces are file-system conventions enforced by nothing. Each stage discovers its own input. The constraint — that the previous stage must have completed and written to the expected path — is invisible. There is no contract at the boundary, only an assumption about what will be there.

In the fallback, I built the mechanism and the config flag. But I left the provenance implicit in the artifact. The constraint — that a fallback run must not produce output indistinguishable from a live run — was never enforced. The fallback worked, but the governing rule that makes it safe to use was nowhere visible.

Every time: the capability was right, the intent was right, and the constraint that keeps it right was left for the reader to infer. That is the same Foundation 2 gap, expressed in Foundation 3 work. I am building the correct things inside invisible boundaries. The boundary is the part I keep omitting.

---

**CustomGPT:**
That's the clearest Foundation 3 pattern.

You are no longer missing the *trade-off*. You are missing the **enforcing signal**.

A constraint that exists only in your head is not governance. It is memory.

**Question:** How did AI affect this pattern in Foundation 3?

Did it help you surface the invisible boundaries, or did it mostly help you build plausible mechanisms faster without forcing the governing constraints into view?

---

**Student:**
Honestly, AI mostly helped me build plausible mechanisms faster without forcing the governing constraints into view.

For each of the concurrency decisions, AI could explain the reasoning clearly: threads for I/O-bound work because the GIL does not block on network waits, processes for CPU-bound work because they bypass the GIL entirely. That reasoning is correct, and AI articulated it well. But AI did not ask "at what scale does this stop being the right choice?" or "what is the measured threshold where thread-creation overhead exceeds the per-request wait?" It answered the implementation question I asked. The governance question I did not ask, AI did not raise.

The same pattern held with the fallback. I asked AI to help implement a sample-data fallback for when the FRED API was unavailable. It produced working code with a configuration flag. It mentioned logging when the fallback activated. It did not say "and here is the architectural rule that keeps this from becoming false assurance." I got a mechanism that worked inside constraints I never stated, which is exactly the weakness this session has been naming.

Where I saw it most clearly was in the documentation. AI-generated documentation in Foundation 3 was consistently too generic; descriptions that could apply to any pipeline rather than this one, with its specific modules, its real output filenames, and its current limitations. I rewrote the README from scratch because the AI version gave the appearance of being explained without actually naming the constraints. That is the same pattern: plausible output that omits the governing specifics.

What AI did not do in Foundation 3 was push back on me. It built what I asked for. The invisible boundaries stayed invisible because I did not ask AI to find them, and AI did not look for them unprompted. The habit I need is to ask the governance question before the implementation question — not "how do I build this?" but "what constraint makes this safe to build, and where does that constraint live?" AI can answer that question when asked. In Foundation 3, I mostly did not ask it.

---

**CustomGPT:**
Good. That is the most mature AI-collaboration analysis you've given across all three foundations.

You identified the real danger:

- AI answers the question you ask
- architecture failures often live in the questions you never asked

And your repeated pattern is now very consistent:

- mechanisms visible
- governing constraints invisible

That is much stronger than Foundation 1, where the lifecycle consequences were discovered only after probing.

---

## Drift Consultation Summary

**Foundation:** 3
**Date:** 2026-05-07
**Topic:** Concurrency trade-offs, stage boundary visibility, provenance handling, and governance constraints in a GDP data pipeline

### Demonstrated Strengths

The student consistently named scope assumptions and invalidation thresholds before probing. Examples included thread overhead versus network latency in kata-05, pickle serialization cost versus computation time in kata-06, and provenance visibility requirements in the sample-data fallback design.

The student demonstrated strong structural reasoning when distinguishing filesystem-based stage sequencing from true interface separation. They identified that the pipeline currently has data-level separation without contract-level separation and explained how that weakens orchestration and isolated testing.

### Areas Needing Development

The student continues to leave governing constraints implicit even when the structural mechanism itself is correct. Across concurrency, fallback behavior, and pipeline boundaries, the "safety rule" existed only as an unstated assumption rather than an enforced or documented constraint.

The student still tends to discover enforcement requirements after implementation rather than encoding them at the point where the architectural decision is introduced.

### Unanswered Questions

- At what measured scale does the thread-pool approach stop fitting relative to asyncio for this workload?
- What is the minimum orchestration structure needed before explicit stage contracts become necessary rather than merely beneficial?
- How should provenance propagate if multiple acquisition sources with different fallback policies are introduced?

### AI Collaboration Assessment

The student showed significantly improved AI-awareness compared to earlier foundations. They identified that AI accelerated mechanism construction while leaving governance questions untouched because those questions were never asked. The student no longer treated AI output as authoritative and recognized that architectural omissions often come from missing prompts rather than incorrect code generation.

### Signals Observed

- **Signal recognition** appeared when the student identified provenance loss as the key architectural weakness in the fallback design.
- **Trade-off awareness** appeared in the analysis of fail-fast errors versus plausible-but-false fallback outputs.
- **Structural judgment** appeared when the student separated filesystem conventions from explicit stage interfaces and identified orchestration pressure at the acquire → transform boundary.
- **Governance reasoning** appeared in the architectural rule: "a fallback run may not produce an artifact indistinguishable from a live run."
- **Intellectual honesty** appeared when the student admitted that the structures were mostly correct while the enforcing constraints remained invisible.

### Commitments for Next Foundation

- Encode governing constraints at the same time mechanisms are introduced.
- Make architectural safety rules visible in artifacts, interfaces, ADRs, or orchestration logic instead of relying on developer memory.
- Ask governance questions before implementation questions when collaborating with AI tools.

**Dimensions Covered:** Signal Recognition, Trade-Off Awareness, Structural Judgment, Governance & Intent
**Estimated Depth:** strong

---

## Drift Session Evaluation

**Foundation:** 3
**Date:** 2026-05-07

| Dimension | Score (1–4) | Points | Evidence |
|---|---|---|---|
| Signal Recognition | 4 | 20/20 | The student consistently identified hidden assumptions, provenance loss, and invisible orchestration boundaries before prompting escalated. |
| Trade-Off Reasoning | 4 | 24/25 | The student clearly analyzed fail-fast versus false-assurance behavior, thread scalability assumptions, and serialization overhead trade-offs. |
| Structural Judgment | 4 | 19/20 | The student distinguished filesystem sequencing from explicit contracts and identified where orchestration pressure concentrates in the pipeline. |
| AI Collaboration | 4 | 19/20 | The student recognized that AI accelerated implementation while leaving governance constraints invisible because the prompts omitted them. |
| Engagement Quality | 4 | 15/15 | The student engaged directly, revised reasoning when challenged, and consistently tied answers back to prior foundations. |

**Total: 97/100**
**Estimated Depth:** strong
**Growth Trajectory:** accelerating

**Priority for Next Foundation:**
Move from recognizing invisible constraints to explicitly encoding them in governance artifacts, interfaces, and pipeline contracts at implementation time rather than after reflection.
