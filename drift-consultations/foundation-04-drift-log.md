# Drift Consultation Log — Foundation 4: Deliver
**Student:** Francis Kelechi Njoku
**Course:** CIDM 6330 — Software Architecture, Spring 2026
**Tool:** Drift Consultation CustomGPT (by Jeffry Babb)
**Session URL:** https://chatgpt.com/g/g-69dabde1bbec8191896617ab0afb625e-drift-consultation
**Date:** 2026-05-07
**Topic:** Governance through tests, test doubles, immutability, and explicit edge-case guards

---

## Full Consultation Transcript

---

**Student:**
Foundation 4 — Deliver.

My Foundation 3 commitment was to move from recognising invisible constraints to explicitly encoding them in governance artifacts, interfaces, and pipeline contracts at implementation time rather than after reflection. I want to test whether the work in Foundation 4 actually shows that, not just whether I can describe it now.

Foundation 4 covered kata-07 (unit testing), kata-08 (test doubles), kata-09 (the complete hardened pipeline), and kata-10 (three TDD cycles plus a bug fix). I will name where I believe constraints were encoded before implementation, and where they were not.

The clearest example of encoding at implementation time is the TDD discipline in kata-10. The RED test for detecting contractions existed before the function existed. That test is a contract — it specifies exactly what the function must return for a known dataset, what it must return when there are no negative growth rates, and that rows with a `None` growth rate must be excluded. The constraint was written before the mechanism, which is the opposite of what I did in Foundations 1 through 3.

The `PeakTrough` dataclass uses `frozen=True`. That is a governing constraint encoded in the interface, not left as a convention. A mutable `PeakTrough` would be technically possible; `frozen=True` makes the immutability rule structural. I applied the same reasoning that was already in `GdpRow` in `pipeline.py` — consistency as a form of governance.

The bug fix in kata-10 is the most direct application of the F3 priority. `generate_report` was crashing on an empty database because `SELECT MIN(value)` returns `NULL` when no rows exist, and formatting `None` with `:.2f` raises `TypeError`. The fix — `if count == 0 or min_v is None` — made a scope assumption visible that had been invisible since kata-04: the pipeline assumed the database would always have rows. That assumption now exists in the code as an explicit guard rather than an implicit expectation.

Where I am less certain is the kata-08 test doubles. I chose not to mock the SQLite database in kata-10 because an in-memory SQLite database is fast and tests the actual SQL. I used test doubles only where the external boundary was genuine — network calls. I believe that was the right discipline, but I want that tested: was that a constraint properly encoded, or was it a judgment call I made without naming the governing rule?

---

**CustomGPT:**
Good. Your framing is already different from Foundation 1.

You are no longer just identifying hidden assumptions after the fact. You are actively asking:

- where was the constraint encoded?
- where does the rule live?
- is the enforcement structural or conventional?

That's a real shift.

Now let's probe the database testing decision.

You said: "I chose not to mock SQLite because an in-memory SQLite database is fast and tests the actual SQL."

That may be correct. But I want the governing rule, not the implementation preference.

**Question:** What is the architectural rule that determines when a dependency should be replaced with a test double versus exercised directly in tests?

Answer the rule first. Then explain how SQLite and the FRED API fall on opposite sides of it.

---

**Student:**
The rule is: replace a dependency with a test double when the dependency's behaviour is outside the test boundary; exercise it directly when the dependency's behaviour is part of what the test is verifying.

That is the complete rule. Everything else follows from it.

The test boundary is the line between what the test is responsible for proving and what it is not. A test double is appropriate when crossing the boundary would make the test non-deterministic, slow, or dependent on external state that the test cannot control. It is inappropriate when using a double would hide the very behaviour the test is supposed to catch.

SQLite and the FRED API fall on opposite sides of that line.

For the FRED API, the behaviour being tested is how my acquisition code handles a response — whether it correctly parses the JSON, applies the fallback when the call fails, and returns the right structure. The network itself is not what I am testing. Whether the FRED service is up at the moment the test runs is outside the boundary. A test that requires a live API call is non-deterministic — it passes when the service is available and fails when it is not, regardless of whether my code is correct. A test double for the FRED API keeps the boundary where it belongs: at my code, not at the external service.

For SQLite, the situation is different. The SQL queries are the behaviour being tested. `detect_contractions` runs `SELECT date FROM gdp_observations WHERE growth_rate < 0 ORDER BY date`. If that query is wrong — wrong column name, wrong condition, wrong ordering — the test should fail. If I mock the database and tell the mock to return two dates, the test passes even if the SQL is syntactically broken. The mock would be hiding the actual behaviour I need to verify. An in-memory SQLite database is fast enough that the cost is negligible, and it exercises the real SQL. There is no reason to introduce a double here because the dependency is deterministic, local, and its behaviour is exactly what the test should be checking.

What I did not do was write that rule down before the tests. I applied the judgment correctly, but it remained an unstated convention rather than a documented constraint. That is the F3 gap still present in kata-08: the rule governed the decisions, but was not encoded anywhere visible. The right place for it would have been a short note in the test module or an ADR section on testing strategy — something that makes the boundary explicit for anyone adding tests later.

---

**CustomGPT:**
Good. That is a defensible rule.

But you caught the weakness yourself: "I applied the judgment correctly, but it remained an unstated convention."

That means Foundation 4 is not asking whether your testing decision was good. It is asking whether the decision **survives you**.

**Question:** If another developer later mocks SQLite "for consistency," what would break in your test suite's ability to govern the architecture?

---

**Student:**
What breaks is the test suite's ability to catch the class of bugs that actually matter in a data pipeline: wrong SQL, schema drift, and unhandled database edge cases.

Here is the specific damage, in order of severity.

The most direct break is SQL correctness. Right now, if I write `SELECT date FROM gdp_observations WHERE growth_rate < 0` and the column is named `gdp_growth_rate`, the test fails. With a mocked database, the mock returns whatever was hardcoded in the test setup, regardless of what SQL was passed. The test passes. The bug ships. The test suite is now proving that the Python logic is correct for given inputs — it is no longer proving that the function correctly retrieves those inputs from the database.

The second break is schema drift detection. If the `gdp_observations` table schema changes and a column is renamed or removed, a real SQLite test fails at the query. A mock test does not know the schema exists. The contract between the analysis functions and their data source becomes invisible to the test suite. Changes to the database layer stop being caught before they reach production.

The third break is the most direct connection to kata-10. The bug that was found — `generate_report` crashing on an empty database because `SELECT MIN(value)` returns `NULL` for empty tables — would never have been discovered if SQLite were mocked. A mock would have returned a number. The `count == 0 or min_v is None` guard would never have been written. That guard is now in the code because the test exercised real SQLite behaviour. Mock it, and the entire class of edge cases involving aggregate functions on empty tables becomes invisible to the test suite.

That is what "governs the architecture" means in this context. The test suite currently enforces a contract: these functions correctly query this database, including in edge cases. If SQLite is mocked for consistency, the suite no longer governs the database layer at all. It governs only the Python logic sitting above it. The architecture has a gap where the data access layer used to be tested, and that gap has no structural signal — the tests still pass, the coverage numbers still look fine, and the governance is gone.

This is the exact consequence of an unstated convention. Another developer mocking SQLite for consistency would not be making a reckless decision — they would be applying a reasonable-sounding rule without knowing the governing reason behind the original choice. The rule needs to be written down so that they will find it before making that change.

---

**CustomGPT:**
Good. You tied the test-double decision to architectural governance, not test style.

A mocked SQLite would preserve coverage while removing the suite's ability to detect database-contract failures. That is exactly the kind of "looks governed, isn't governed" failure Foundation 4 is about.

**Question:** Where should this testing rule live so it survives another developer's reasonable-but-wrong "mock everything for consistency" instinct?

---

**Student:**
It should live in two places, for the same reason I identified in Foundation 2 with the `RuntimeError` threshold — different audiences need the governance signal at different moments.

The first is an ADR. The decision to exercise real SQLite rather than mock it is an architectural decision: it determines what class of failures the test suite can detect. An ADR would record the rule itself, the reasoning behind it — SQL correctness, schema drift detection, NULL aggregate behaviour — and the exact threshold where the decision would need to be revisited. That threshold is not "when another developer prefers mocks." It is something measurable: if the in-memory SQLite tests became slow enough to block the test run, or if the analysis module required a database feature that in-memory SQLite does not support. An ADR captures the why and the invalidation condition, not just the what.

The second is a comment at the top of the test module or the `conftest.py` where the in-memory database fixture is defined. Not a docstring explaining what the fixture does — that is already visible from the code. A short note explaining why it is real SQLite and what would be lost by substituting a mock: the suite would no longer verify SQL correctness, schema changes would stop being caught, and the class of bugs involving NULL aggregates on empty tables would become invisible. That note is at the threshold. A developer adding tests encounters it before making the substitution, not after reading an ADR they may not know exists.

Those two places serve different purposes. The ADR is the governance record — it exists for someone making an architectural decision about the testing strategy. The call-site note is the implementation warning — it exists for someone touching the test code who may never think to look for an ADR.

What I did not do in kata-10 is write either of them. The rule governed the decision, but was not encoded anywhere it would be found. The in-memory SQLite fixture exists in `conftest.py`, the tests pass, and nothing in the test files explains why a real database is used instead of a mock. That is the same gap Foundation 3 named: a constraint that exists only in the developer's head is not governance. It is memory. This session is the first time the rule has been written down, and it is written in a consultation log rather than in the codebase, where it would actually protect anything.

---

**CustomGPT:**
Good. You've identified the exact Foundation 4 gap:

The rule exists, but it does not yet **survive outside your memory**.

Now let's test one more governance surface.

You said `frozen=True` makes immutability structural.

**Question:** What architectural risk does immutability reduce in your analysis/reporting module, and what does it sacrifice?

---

**Student:**
Immutability reduces the risk of computed results being silently modified after they are created. What it sacrifices is the ability to build or enrich those results incrementally.

Here is the specific risk it reduces in the analysis module.

`PeakTrough` is a derived result — it is computed from the database state at a specific moment and passed downstream to `generate_summary_report`. Without `frozen=True`, any function that receives the object could modify its fields before the report is generated. The modification might be accidental — a developer adding enrichment logic who does not realise the object should be read-only — or it might be a future feature that mutates the object in place rather than creating a new one. Either way, the report would be generated from a `PeakTrough` that no longer represents what was computed from the database. The object would have drifted from its source.

`frozen=True` makes that class of drift structurally impossible. A downstream function that tries to modify the peak or trough value raises a `FrozenInstanceError` at runtime. The constraint is enforced by the interface, not by developer discipline. That is the same principle as the SQLite testing decision: structural enforcement is more durable than convention.

The connection to `GdpRow` in `pipeline.py` is deliberate. A row read from a CSV source should not change after it is created — the data it represents is fixed at the point of extraction. A `PeakTrough` computed from the database is the same: it represents a point-in-time calculation. Once computed, it should not be a mutable object that floats through the pipeline accumulating changes. Making both dataclasses frozen creates a consistent signal: objects of this type are snapshots, not working state.

What `frozen=True` sacrifices is incremental construction. If I needed to build a `PeakTrough` in two passes — compute the peak in one step, compute the trough in a separate step, then attach them to the same object — I cannot do that with `frozen=True`. Every field must be valid at construction time, and the object is sealed at that point. For the current design, this costs nothing: `compute_peak_trough` produces both values in a single query and returns a complete object. But if a future version of the module needs to enrich `PeakTrough` with an additional computed field after creation, the frozen constraint means a new instance must be created rather than the existing one being updated in place.

The trade is worth it for the current scope. The risk of silent mutation in a reporting pipeline is higher than the cost of constructing complete objects. That assessment changes if the analysis module grows to the point where incremental construction is genuinely needed, which is the threshold where `frozen=True` would need to be reconsidered.

---

**CustomGPT:**
Good. You defended `frozen=True` as a constraint, not decoration.

You also named its cost: no incremental enrichment without creating a new object. That is acceptable because the object represents a computed snapshot.

Now final probe before closing:

**Question:** Across TDD, real SQLite tests, `frozen=True`, and the empty-database guard, what changed from Foundation 3 to Foundation 4?

Name the change in your architectural behavior, not the artifacts.

---

**Student:**
What changed is where the constraint lives. In Foundations 1 through 3, constraints existed in my reasoning. In Foundation 4, they began existing in the code.

In Foundation 3, the weakness was: I built correct structures, but left the governing rule implicit. The mechanism was right, the intent was right, and the constraint that kept it right was left for the reader to infer. The test suite, the fallback, the stage separation — all of them worked inside invisible boundaries.

In Foundation 4, the sequence changed in at least three places.

In the TDD cycles, the constraint was written before the mechanism existed. The RED test for `detect_contractions` specified the contract — what must be returned for known data, what must be returned for empty data, what must happen to `None` growth rates — before the function was written. That is not recognising a constraint after the fact. That is encoding it first and building the mechanism to satisfy it. The order of operations changed.

With `frozen=True` on `PeakTrough`, the immutability rule is part of the interface. A developer receiving a `PeakTrough` object does not need to know that it should not be modified — the dataclass raises an error if they try. The constraint does not depend on the developer reading the code correctly. It enforces itself.

With the empty-database guard, an invisible scope assumption that had been present since kata-04 became a visible condition in the code. The pipeline assumed non-empty rows. That assumption was never stated. The bug made it visible, and the fix encoded it explicitly: `if count == 0 or min_v is None`. The assumption is now in the code rather than in the developer's memory.

What did not change is the documentation layer. The rule about SQLite versus test doubles was applied correctly, but not written into an ADR or a call-site note. The reasoning exists in this consultation and in my own understanding, but not in a place where another developer would encounter it before making the wrong choice. That is the part of the F4 commitment that was not met. The code-level encoding improved. The governance-artifact encoding did not.

So the change in architectural behaviour is real but incomplete. I moved from constraints living only in reasoning to constraints living in code. I have not yet consistently moved to constraints living in governance artifacts. That gap is what this session has been naming.

---

## Drift Consultation Summary

**Foundation:** 4
**Date:** 2026-05-07
**Topic:** Governance through tests, test doubles, immutability, and explicit edge-case guards

### Demonstrated Strengths

You showed real growth by moving constraints from reasoning into code. TDD made behaviour contracts exist before implementation, `frozen=True` encoded immutability structurally, and the empty-database guard made a hidden assumption explicit.

### Areas Needing Development

Your code-level governance improved, but documentation-level governance remains incomplete. The SQLite-versus-mock testing rule was applied correctly but not preserved in an ADR, fixture comment, or testing strategy note.

### Unanswered Questions

- When should testing strategy decisions become ADR-level decisions?
- What other test-suite rules are currently conventions rather than governance?
- Where should future developers encounter architectural testing constraints before violating them?

### AI Collaboration Assessment

Your AI collaboration appears mature. You are no longer just accepting mechanisms; you are evaluating whether constraints survive outside your memory.

### Signals Observed

- **Signal recognition** appeared when you identified which constraints were encoded in code and which remained only in memory.
- **Trade-off awareness** appeared in your analysis of real SQLite tests versus mocks, immutability versus incremental enrichment, and fail-safe guards versus assumed valid data.
- **Structural judgment** appeared when you distinguished structural enforcement from convention through TDD contracts, frozen dataclasses, and database-backed tests.
- **Governance reasoning** appeared when you identified that the SQLite testing rule needed to live in both an ADR and a call-site note to serve different audiences.
- **Intellectual honesty** appeared when you named the remaining documentation gap without defensiveness.

### Commitments for Next Foundation

Carry governance beyond code by documenting testing rules, invalidation thresholds, and architectural constraints where future maintainers will encounter them.

**Dimensions Covered:** Signal Recognition, Trade-Off Awareness, Structural Judgment, Governance & Intent
**Estimated Depth:** strong

---

## Drift Session Evaluation

**Foundation:** 4
**Date:** 2026-05-07

| Dimension | Score (1–4) | Points | Evidence |
|---|---|---|---|
| Signal Recognition | 4 | 20/20 | You identified which constraints were encoded in code and which remained only in memory. |
| Trade-Off Reasoning | 4 | 24/25 | You explained real SQLite tests versus mocks, immutability versus incremental enrichment, and fail-safe guards versus assumed valid data. |
| Structural Judgment | 4 | 19/20 | You distinguished structural enforcement from convention through TDD contracts, frozen dataclasses, and database-backed tests. |
| AI Collaboration | 4 | 19/20 | You demonstrated mature judgment by focusing on whether AI-assisted work produced durable constraints, not just working artifacts. |
| Engagement Quality | 4 | 15/15 | You answered directly, self-corrected, and named the remaining governance gap without defensiveness. |

**Total: 97/100**
**Estimated Depth:** strong
**Growth Trajectory:** mature

**Priority for Next Foundation:**
Move from code-enforced constraints to durable governance: write the ADRs and test-module notes that make your architectural rules survive another developer.
