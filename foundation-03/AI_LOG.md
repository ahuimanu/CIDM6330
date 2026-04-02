# AI_LOG

## Foundation 3

### Process Description
- I used AI primarily for project scaffolding, implementation planning, draft code generation, and documentation structure.
- I worked iteratively: define the deliverable, ask AI for a practical implementation path, run the code locally, then revise anything that was too generic or did not fit the GDP/FRED pipeline scope.
- I did not accept AI suggestions blindly. I treated AI output as a starting point and verified behavior by running the pipeline and unit tests.

### Decision Log
- Decision: keep Foundation 3 as a modular monolith instead of distributing components.
	- Asked AI: whether to start with a service split or a local pipeline.
	- AI suggested: keep the first MVP local and modular because working code matters more than premature infrastructure.
	- What I did: accepted the modular local pipeline approach.
	- Why: it fits the assignment scope and makes iteration evidence easier to show.

- Decision: use sample GDP data by default with optional live FRED mode.
	- Asked AI: how to keep the code runnable without depending on external network access.
	- AI suggested: add a sample payload path and allow live API mode when an API key exists.
	- What I did: accepted and implemented that design.
	- Why: it guarantees runnable code for grading while still showing a realistic FRED integration path.

- Decision: output raw and transformed JSON files instead of adding a database in Foundation 3.
	- Asked AI: whether SQLite should be introduced immediately.
	- AI suggested: defer database output and keep artifacts inspectable in files.
	- What I did: accepted that suggestion for Foundation 3.
	- Why: it keeps the MVP simple and makes transformation results easy to inspect in the repo.

- Decision: add retry/backoff and fallback behavior for live FRED acquisition.
	- Asked AI: how to strengthen API/network/rate-limit handling without over-engineering the MVP.
	- AI suggested: configurable retries, exponential backoff, and optional fallback to sample payload.
	- What I did: accepted and implemented this pattern in acquisition/config.
	- Why: it improves reliability and aligns better with the assignment rubric while keeping the pipeline runnable.

### AI Failures
- AI initially generated documentation that was too generic and not tied closely enough to my actual GDP/FRED code. I rewrote the docs to reference the real modules, outputs, and current limitations.
- AI also tended to suggest broader architecture options, including more structure than the assignment needed. I reduced that to a practical modular pipeline because working code was more important than speculative design.
- In earlier work during Foundation 3, AI-generated git and PR suggestions needed adjustment because they were not always aligned with my instructor's requirement that each assignment be submitted individually.

### Verification Practices
- I verify AI-generated code by running the pipeline locally with `python -m pipeline.run_pipeline`.
- I verify correctness at a basic level by running `python -m unittest discover -s pipeline/tests -p "test_*.py"`.
- I inspect generated artifacts in `data/raw`, `data/transformed`, and `output/reports` to confirm the pipeline produced the expected files.
- I compare documentation claims against the current implementation before treating them as final submission content.

### Judgment Patterns
- I usually override AI when it introduces more complexity than the assignment needs.
- I also override AI when suggestions are too abstract and not grounded in the current codebase.
- A recurring pattern is that AI is useful for generating first drafts quickly, but I need to tighten scope, remove unnecessary architecture, and align the final work to the exact rubric language.

## Foundation 4

### Process Description
- I used AI to convert the Foundation 3 implementation into a defendable Foundation 4 submission.
- The collaboration focused on gap analysis against the lecturer rubric, strengthening automated tests, improving alignment to the original Foundation 2 problem statement, and producing architecture-defense artifacts.
- I kept the final judgment on scope. When AI suggested broader options, I filtered them through the Foundation 4 expectation that the MVP must run and the architecture must be explainable.

### Decision Log
- Decision: keep the existing Foundation 3 codebase as the MVP base rather than starting a new project.
  - Asked AI: whether Foundation 4 should be a new implementation or a delivery-and-defense layer over Foundation 3.
  - AI suggested: promote the existing GDP/FRED pipeline into the final MVP and close the gaps around testing, ADRs, diagrams, and reflection.
  - What I did: accepted that approach.
  - Why: it fits the lecturer's framing of Foundation 4 as deliver, document, and defend.

- Decision: add derived GDP indicators to better match the Foundation 2 problem statement.
  - Asked AI: how to close the gap between cleaned GDP records and the promised trend-monitoring output.
  - AI suggested: extend transformation to compute GDP level, QoQ, YoY, rolling 4-quarter change, and simple signal flags.
  - What I did: accepted and implemented those indicators.
  - Why: it made the MVP more faithful to the original business problem and stronger in defense.

- Decision: write richer ADRs instead of relying on the thin Foundation 3 ADRs.
  - Asked AI: how to make the ADRs match the lecture guidance about rationale, alternatives, and consequences.
  - AI suggested: create Foundation 4 ADRs centered on dataset choice, style choice, technology choice, and explicit trade-off resolutions.
  - What I did: accepted and expanded the ADR set.
  - Why: the lecturer emphasized that ADR quality matters more than quantity.

- Decision: use a technical-audience Mermaid diagram rather than a broader all-purpose diagram.
  - Asked AI: what kind of diagram best fits the assignment and lecture notes.
  - AI suggested: one clear technical-colleague view with labels, title, and legend rather than mixing audiences.
  - What I did: accepted that approach.
  - Why: it aligns with the lecture point that one diagram should serve one audience and one abstraction level.

### AI Failures
- AI still tends to over-document or over-architect when the assignment could be satisfied with a narrower MVP.
- Some first-draft tests had incorrect expected values because the logic had to be checked carefully against real formulas.
- AI can draft ADRs quickly, but I still need to ensure the decisions are true to what the code actually does rather than what sounds architecturally impressive.

### Verification Practices
- I verified the enhanced MVP by running `python -m pipeline.run_pipeline`.
- I verified automated testing with `python -m unittest discover -s pipeline/tests -p "test_*.py"`.
- I checked the generated JSON and markdown outputs to ensure the reported metrics and flagged periods matched the implemented logic.
- I compared the final artifacts against the lecturer's Foundation 4 checklist before treating the submission package as complete.

## Overall Assessment Across All Four Foundations

### Where AI Was Most Helpful
- Turning rubric language into an actionable checklist
- Drafting code scaffolds and test cases quickly
- Surfacing trade-offs and documentation structure for ADRs and reflections
- Helping me iterate on explanations, especially when aligning technical output to course expectations

### Where AI Was Least Helpful or Misleading
- When it proposed unnecessary complexity beyond the assignment scope
- When it produced generic documentation that was not tightly grounded in my real codebase
- When it suggested architectural options that sounded sophisticated but were not justified by the project scale

### How My AI Collaboration Evolved
- Early on, I used AI more for exploration and idea generation.
- By Foundations 3 and 4, I used AI more as a drafting and verification partner while I kept tighter control over scope, architecture, and final wording.
- My process became more disciplined: inspect the repo, compare against rubric, implement, verify locally, then document only what is actually true.

### What I Would Do Differently Next Time
- Start ADR writing closer to the moment of decision rather than reconstructing rationale later
- Keep a more explicit running gap list between the original problem statement and the current MVP
- Introduce verification earlier for any AI-generated formulas or test expectations

### Recommendation to a Colleague Starting an AI-Assisted Architecture Project
- Use AI to accelerate drafts, comparison, and structure, but do not let it choose scope for you.
- Keep decisions tied to concrete constraints, not to fashionable patterns.
- Verify every important claim in code, tests, and documentation.
- Treat AI as a collaborator for momentum, not as a substitute for architectural judgment.
