# Architecture Style 

## Selected Style: 
    *Pipeline Architecture

## Why this Style: 
    * Supports Audibility: In a Pipeline architecture, data transitions through discrete "pipes" between independent "filters" (the transformation steps). This property inherently supports Auditability because we can attach a logging mechanism to the end of every filter, capturing the exact state of the JSON payload at every stage of the math without disrupting the flow. 
    * Support Data Integrity: The strict, unidirectional flow of a Pipeline guarantees the order of operations—the $S$ score calculation physically cannot run until the data has passed through the normalization filter. Furthermore, we can insert a dedicated "Validation Filter" immediately before the final calculation that acts as a strict gatekeeper, throwing a fatal error if any upstream variable arrives as a raw number rather than a percentage.

## Alternatives considered:

    *Microservices architecture was strongly considered but ultimately rejected because it actively works against core characteristics of Testability and Data Integrity.

        **Dependency Problem: The mathematical transformations are strictly sequential (e.g., the Rolling Average calculator is entirely dependent on the completion of the Percent Change calculator). Separating these into independent microservices creates tight behavioral coupling across a network.
        
        **Testability & Integrity Risks: If microservices were used, testing the $S$ score calculation would require spinning up multiple independent network services and mocking complex network calls. Furthermore, introducing network latency between mathematical steps introduces massive Data Integrity risks (ex: what happens if the network drops the data payload between the Normalization service and the Aggregation service?).

## Style-specific trade-offs:

    *Trade-off Accepted: Reliability and Fault ToleranceThe primary cost of choosing a Pipeline Architecture is a reduction in system Reliability. Because the architecture dictates a strict, sequential flow of data, a failure in any single filter will halt the entire process, resulting in no output for that batch run.
    
    *Why this is acceptable: This system is explicitly trading Reliability to guarantee Data Integrity. A loud failure (the pipeline halting) is vastly preferable to a silent failure (the pipeline bypassing a broken normalization step and outputting a mathematically invalid $S$ score). Furthermore, because this is a monthly batch job with a 3-to-6 month lead time, a temporary pipeline crash is easily mitigated by fixing the bug and re-running the job the next day.

## Quantum analysis:

    *Architecture Quanta: 1
    
    *Why: The Shortage Scout system consists of a single architecture quantum. The entire pipeline (Ingestion --> Normalization --> Aggregation --> Calculation --> Output) possesses extremely high functional cohesion as it exists to achieve exactly one business goal (generating the monthly "OVERBUY" or "HOLD" recommendation).The system acts as a single, independently deployable artifact (i.e a single packaged Python script). Because the mathematical filters must execute synchronously and sequentially to produce any valid output, they cannot be split into separate deployable quanta without destroying the system's core functionality