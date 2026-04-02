# Architecture Reflection

## What Changed

My Foundation 2 design described a full extract-validate-transform-load-report pipeline for Real GDP trend monitoring. By the end of Foundation 4, the architecture is still a pipeline, but the implemented MVP is more concretely a modular monolith with explicit Python modules for acquisition, transformation, reporting, configuration, and orchestration.

The biggest change is that implementation forced sharper scope control. In Foundation 2 I described CSV and/or SQLite persistence plus several analytical outputs. In Foundation 4 I kept the runtime simpler by using JSON artifacts and a markdown summary report, while still adding the trend indicators that were central to the original problem: GDP level, quarter-over-quarter change, year-over-year change, trailing four-quarter change, and simple downturn-style flags.

## What I Learned

I understand much more clearly now that architecture is not just choosing a style. It is sustaining decisions through documentation, communication, and evidence. A pipeline style sounded correct in Foundation 2, but Foundation 4 made me prove that the style still fit after real implementation constraints appeared.

I also understand the lecturer's point that patterns and decisions are trade-off bundles. "Pipeline" was not the answer by itself. I still had to explain what I gained from that choice and what I paid for it. The same was true for sample-mode defaults, JSON outputs, and keeping the project as a modular monolith instead of pushing it into unnecessary distribution.

## Trade-offs Revisited

The Foundation 2 driving characteristics were analytical accuracy, reproducibility, and data quality/consistency. Those held up. In practice:

- Accuracy mattered more than speed. I spent more effort on transformation rules, ordering, and derived metrics than on performance.
- Reproducibility mattered more than realism. Defaulting to sample mode made the MVP dependable for grading and testing, even though live FRED access is more realistic.
- Data quality required explicit filtering and signal rules. Without those decisions, "working code" would still produce weaker analysis.

What surprised me most was how much documentation quality affects architecture quality. Thin ADRs and vague diagrams look complete at first, but they do not survive questioning. The lecture notes were right: if a future reader cannot understand the rationale, the architecture has not really been preserved.

## If I Started Over

I would align implementation artifacts to the Foundation 2 problem statement earlier. The first MVP successfully fetched and cleaned GDP data, but it did not yet deliver enough analytical output to fully match the promised trend-monitoring problem. I corrected that in Foundation 4 by adding derived metrics and flagged periods.

I would also start ADR writing earlier and treat it as part of development rather than end-stage documentation. Writing ADRs after implementation is still useful, but writing them closer to the decision point would have captured more alternatives and rationale with less reconstruction effort.
