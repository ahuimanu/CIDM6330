# AI Collaboration Log

## Foundation 1

### What I Asked
* Compare BTS, BLS, and FRED datasets.
* Refine the problem space to focus specifically on Hardware OEMs (Dell, HP, Lenovo).
* Identify business-specific FRED series for Pricing, Supply Chain, and Demand Forecasting.
* **Task:** Develop a FRED fetch script and a helper script to manage API keys and determine file types (CSV vs. JSON) for ingestion.

### What I Got
* Strategic business cases for FRED data (e.g., using `FEDFUNDS` to predict refresh cycles).
* Structured Markdown templates for Foundation 1.
* A Python helper strategy for managing the FRED API's authentication and data retrieval constraints.

### What I Used, Modified, or Rejected
* **Used:** The concept of "Leading Indicators" for supply chain risk.
* **Used:** The "Margin Protector" business case.
* **Modified:** Shifted the focus from general "Finance" to "Hardware OEM Strategy" to increase the potency of the project.
* **Added:** Specifically added a task to build a modular fetch and helper script for the data pipeline.

### My Judgment Calls
I prioritized **Interpretability** as a core architecture characteristic. Because this system is designed for business managers, the architecture cannot be a "black box"; it must provide the lineage of the data (Series ID and Revision date) for every recommendation.

## Foundation 2

### What I Asked
    *I asked the AI to help me narrow down my broad list of architecture characteristics to the top three driving forces for the "Shortage Scout" system.

    *I requested help defining strict, measurable goals for those top three characteristics (Auditability, Data Integrity, and Testability).

    *I asked for an architecture style recommendation that would physically support my mathematical pipeline.

    *I challenged the AI to evaluate alternative styles (like Microservices and Service-Based architectures) and specifically asked it to analyze the "Distributed Monolith" anti-pattern.

### What I Got
    *Problem Refinement: The AI helped filter out irrelevant operational characteristics (like Scalability and Elasticity) by reminding me this is a low-traffic, monthly batch job.

    *Corrections: It corrected my initial confusion between a Reliability failure (the system crashing) and a Data Integrity failure (the system silently outputting bad math).

    *Style Recommendation: It strongly recommended the Pipeline Architecture (Pipes and Filters) to enforce strict, sequential data transformations.

    
### What I Used, Modified, or Rejected
    *Used: I used the AI's recommendation for the Pipeline architecture and its formal definitions for Component Identification (Technical Partitioning, Functional Cohesion).

    *Modified: I modified the AI's basic rejection of Microservices by forcing an analysis of Service-Based architectures, allowing me to write a much more academically rigorous "Alternatives Considered" section.

    *Rejected: I actively rejected the need for high Reliability or distributed components. I accepted the Pipeline's trade-off that failing loudly (crashing) is significantly safer than failing silently and outputting an incorrect financial recommendation.

### My Judgment Calls
    *Matching Shape to Problem: I made the definitive architectural call that because my core problem is a linear mathematical equation (Percent Change $\rightarrow$ Rolling Average $\rightarrow$ $S$ Score), the physical architecture must match that linear shape.

    *Avoiding Anti-patterns: I determined that artificially splitting sequentially dependent mathematical steps into separate networked services provides zero business value and introduces massive data integrity risks.
    
    *Enforcing Testability: I judged that strictly enforcing fast, isolated unit tests was the only way to mathematically guarantee the "OVERBUY" recommendation would be accurate before the business spent millions of dollars on inventory.

## Foundation 3

### Process description
* Workflow: I will iterate in small MVPs: (1) Data Acquisition, (2) Data Transformation, (3) Pipeline Integration. I invoke AI for design suggestions, short code snippets (2-10 lines), and for checklist/review tasks. I avoid asking AI to write entire assignment solutions; I use it to accelerate repetitive tasks and clarify errors.
* When I invoke AI: design questions, API usage, debugging hints, and small helper functions. When I work independently: core algorithm design, test assertions, final acceptance criteria.

### Decision log (selected entries)
* What I asked: "Propose a robust acquisition pattern for monthly FRED series, with retries and file output."
* What it suggested: A fetch-all function that saves per-series CSVs and a combined CSV, with basic error handling.
* What I did: Implemented `Foundation3/acquire.py`, adding retries and clear error messages; wrote a unit test that mocks `get_fred_series`.
* Why: To ensure reproducible, testable acquisition without relying on external network access during CI.

### AI failures
* Example: An earlier AI suggestion attempted to call the FRED API without checking for `FRED_API_KEY`. I rejected that and added an explicit env check and clearer error guidance.

### Verification practices
* Unit tests: mock external calls (e.g., `get_fred_series`) and assert files and combined outputs are produced.
* Manual run: run the pipeline locally with a valid `FRED_API_KEY` in `.env` and inspect `Foundation3/results/`.

### Judgment patterns
* I override AI suggestions that perform network I/O in tests; instead I prefer dependency injection or mocking.
* I accept AI suggestions for small helper functions, logging patterns, and README scaffolding.

---

### Foundation 3 — Implementation log (ongoing)

Recent work completed:

* Added a robust acquisition module: `Foundation3/acquire.py` with retries, per-series CSV output, and combined CSV output.
* Added transformation logic in `Foundation3/transform.py` that computes month-over-month percent change, a 3-month rolling mean, a weighted `S_score`, and an automatic `Recommendation` field.
* Integrated pipeline runner `run_pipeline.py` that runs in demo mode (synthetic data) when `FRED_API_KEY` is not present, or performs real acquisition when the key is available.
* Created `Foundation3/generate_sample.py` to produce deterministic sample outputs and `Foundation3/results/transformed.json` for deliverables and inspection.
* Added unit tests: acquisition test (`Foundation3/tests/test_acquire.py`), transform tests (`test_transform.py`, `test_transform_weights.py`) to validate core logic and weights behavior. All tests pass locally.
* Improved logging: `Foundation3/pipeline.py` and `Foundation3/acquire.py` now emit informative run logs and record shapes/counts for observability; demo runs write `Foundation3/results/pipeline.log`.

How I validated changes:

* Tests were executed locally using the repository virtual environment (`pytest`).
* Demo pipeline run created `Foundation3/results/transformed.json` and `pipeline.log` confirming end-to-end flow without network access.

Next verification steps I recommend:

1. Add GitHub Actions CI to run `pytest` on push/PR (keeps tests green).
2. Manually run `python run_pipeline.py` with a valid `FRED_API_KEY` in `.env` to verify real acquisition.
3. Expand transformation tests to match final scoring formula as it evolves.

Notes on AI collaboration during this work:

* What I asked the AI: Suggested small, testable code patterns, logging formats, and a file-based demo mode to avoid exposing API keys in CI.
* What I accepted: Short code snippets, test patterns, and the plan to iterate in MVPs.
* What I rejected or changed: Replaced any AI-suggested direct network calls in tests with mocking; required explicit env-key checks before live runs.

### CI and Docs updates
* What I asked: "Add CI that runs tests on push/PR and does not require API keys."
* What it suggested: A GitHub Actions workflow that installs dev requirements and runs `pytest`.
* What I did: Added `.github/workflows/ci.yml` which installs `requirements-dev.txt` (if present) and runs tests. Updated `Foundation3/README.md` with CLI usage and CI notes. Added `ARCHITECTURE.md` summarizing architecture decisions.

### Reflection
* The AI helped accelerate small, repeatable edits (README snippets, CLI examples). I reviewed and adapted suggestions to meet course constraints (no secrets in CI, small focused tests).

---

## Foundation 4

### What I Asked
* To help me formalize seven Architecture Decision Records (ADRs) covering the key design choices made across the project: series selection, pipeline style, file-based output, fail-fast error policy, NaN handling, asymmetric PPI weighting, and raw-payload archiving.
* Asked the AI to help me structure an Architecture Reflection that honestly traced how the F2 design changed through F4 implementation — what gaps were corrected, what was learned, and what I would do differently.
* Asked the AI to help me diagnose a broken test: `test_acquire.py` was monkeypatching `get_fred_series`, a name that no longer existed in `acquire.py` after the module was upgraded to use `get_fred_series_with_payload`.
* Asked to help me assemble the two milestone deliverables — `MVP_Completion.md` and `Test_Coverage.md` — by organizing working code evidence, data samples, error handling documentation, and an honest coverage map into a coherent format.

### What I Got
* A template-driven ADR structure (frontmatter, Intent, Decision, Consequences, Alternatives Considered, Requirements Checklist) that I used to document all seven decisions consistently.
* A four-section reflection outline — what changed, what was learned, trade-offs revisited, and "if I started over" — that gave me a scaffold for turning raw observations into a structured retrospective.
* A precise diagnosis of the test failure: the monkeypatch target needed to be `acq.get_fred_series_with_payload`, and the fake's return type needed to change from a bare `df` to a `(df, payload)` tuple to match the upgraded interface.
* Drafts of `MVP_Completion.md` and `Test_Coverage.md` organized around the actual module structure, which I reviewed and corrected against the live codebase.

### What I Used, Modified, or Rejected
* **Used:** The ADR structure as provided. The decisions themselves — especially ADR-006 on asymmetric PPI weight and ADR-007 on raw JSON archiving — were my own, grounded in the F3 risk log; the AI helped me articulate them in a consistent, reviewable format.
* **Used:** The test fix exactly as diagnosed. The root cause (wrong monkeypatch namespace) was real, the correction was minimal, and I verified it against the actual module before accepting it.
* **Used:** The Architecture Reflection structure. I wrote the content of each section myself; the AI helped me organize and sharpen the language.
* **Modified:** `MVP_Completion.md` and `Test_Coverage.md` were adjusted to reference the actual file paths, test names, and assertion text from the live codebase rather than generic stand-ins the AI produced.
* **Rejected:** Any AI suggestions to expand test coverage or add features as part of Foundation 4 — this milestone was a documentation and retrospective checkpoint, not a feature sprint.

### My Judgment Calls
* I treated the three "if I started over" corrections in the Architecture Reflection as the most important deliverable of the entire milestone. All three are traceable to concrete failures (Risk 4, Risk 7, Risk 9 from F3): raw archiving was deferred too long, the PPI weight was written correctly in F2 but never enforced in code, and the validation filter sat in the design document for two milestones before it was built. I made the deliberate choice to present these gaps honestly rather than retrospectively frame them as planned iterations.
* I confirmed that the logical five-filter architecture and the physical three-file implementation are not a contradiction — they are a deliberate consolidation. Forcing one file per conceptual filter would have made the code harder to test without making the architecture more correct.
* I kept the test coverage section's "not covered" table honest. Retry/back-off, the strict NaN path, and the range-validation guard are real gaps. I judged that acknowledging them is more architecturally useful than closing them with shallow tests to inflate a coverage number.

