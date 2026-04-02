# ADR-002: Keep the MVP as a Modular Monolith Pipeline

## Status

Accepted

## Context

Foundation 2 selected a pipeline architecture because the problem is sequential: acquire data, validate/normalize it, transform it into indicators, persist outputs, and report results. During Foundations 3 and 4, implementation experience showed that the system is still small, single-user, and easiest to run locally.

Alternatives considered in context:

- Split the stages into separately deployed services
- Introduce asynchronous messaging between acquisition and transformation
- Use a more generic layered application structure

The service and messaging alternatives would add infrastructure, deployment, and operational complexity without solving a pressing problem in the current scope. A generic layered design would be less aligned with the data-flow nature of the work than an explicit pipeline.

## Decision

Keep the delivered MVP as a modular monolith organized around pipeline stages. The modules remain separate by responsibility, but they execute together in one local runtime. This preserves the pipeline benefits from Foundation 2 while matching the implementation reality discovered in Foundations 3 and 4.

## Consequences

Positive:

- Simple local execution and grading
- Low operational overhead
- Clear mapping from course problem to code structure
- Easier automated testing because the whole system can run offline in one process
- Better fit with current team size and course scope

Negative:

- Independent scaling of stages is not available
- `run_pipeline` becomes a coordination hotspot if too many concerns accumulate there
- Future distribution would require new boundaries for deployment, monitoring, and failure handling
