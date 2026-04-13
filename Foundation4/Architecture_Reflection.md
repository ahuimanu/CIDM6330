# Architecture Reflection — Foundation 1 through Foundation 4

---

## 1. What Changed: Foundation 2 Design → Foundation 4 Final

**The structure simplified, and three gaps in the design got fixed.**

Foundation 2 described five logically separate components: Ingestion, Normalization, Aggregation, Calculation, and Enrichment/Output. Foundation 4's actual architecture is still five **filters**, but three of them (Normalization, Aggregation, Calculation) live inside a single `transform.py` module. The ARCH_REALITY_CHECK.md explains the deliberate reason: those three operate on the same DataFrame in sequence — separating them into files would have added import complexity with zero testability benefit.

Beyond consolidation, three substantive corrections were made that weren't in the F2 design:

| F2 Design | F4 Reality | Why It Changed |
|---|---|---|
| Validation Filter was specified but absent | Filter 3 (`ValueError` on values outside `[-1.0, 1.0]`) added — ADR-004/005 | F3 identified this as Risk 9: the exact Data Integrity failure the architecture was designed to prevent |
| Equal positive weights on all four series | `PCU334413334413` gets `−1.0` weight — ADR-006 | F3 Risk 7: rising prices were being treated as a *good* supply signal, directly contradicting the stated formula |
| No raw payload archiving | Timestamped `{series_id}_{timestamp}.json` archive written at acquisition — ADR-007 | F3 identified FRED retroactive revisions as the largest unresolved architectural risk (Risk 4) |

The quantum count stayed at 1. The Pipeline style was validated by implementation and held throughout. The big story is not style change — it's that three design bugs introduced in Foundation 2 were discovered and corrected by Foundation 4.

---

## 2. What You Learned

**Specific things that weren't visible from the design phase:**

- **Logical vs. physical architecture don't have to match.** You can have five conceptual filters and three files. Architecture is about sequencing and responsibility, not file count. Trying to force five files would have made the code worse without making the architecture cleaner.

- **Silent failures are a design problem.** The S_score weighting error in F3 (Risk 7) was not a crash — it was producing *plausible but wrong* recommendations. The architecture's entire Data Integrity characteristic exists to prevent this category of failure. Designing for loud failure (ADR-004) is an active choice, understood as a structural commitment, not just good practice.

- **Auditability has a precise meaning that design documents can blur.** F2 said "log intermediate artifacts." F3 discovered that logging derived CSVs doesn't capture what FRED returned on a specific day, because FRED revises history. True point-in-time auditability requires archiving the raw response before any parsing. These feel like the same thing until someone was to try and reconstruct a past decision.

- **Python import mechanics matter architecturally.** Monkeypatching `Foundation3.acquire.get_fred_series` vs `Foundation1.FRED_helper.get_fred_series` — the patch must target where the name is *used*, not where it's *defined*. This was a great example of how component boundaries manifest in code differently than they appear in a component diagram.

- **NaN handling is a business rule, not a cleanup step.** `dropna(how="all")` vs `dropna(how="any")` encodes a domain decision: do you allow a score from 3/4 series near a month boundary, or do you refuse to score at all? That's not a data-cleaning detail but moree so an architecture decision (ADR-005).

---

## 3. Trade-offs Revisited

**Looking back at the F2 characteristic trade-offs:**

**Reliability vs. Data Integrity — played out exactly as designed, but the real cost was sharper than expected.**

F2 accepted that "a failure in any single filter will halt the entire process." This was formalized in ADR-004. What wasn't fully anticipated: a transient FRED network timeout on *one* of four series now aborts the entire run, even when the other three fetched successfully. The loud failure is still the right call — the alternative (scoring on 3/4 series silently) is the exact failure mode the architecture prevents. But the operational cost (manual re-trigger on every transient failure) is more noticeable than the design made it sound.

**Flexibility vs. Complexity — resolved more cleanly than expected.**

F1 asked whether a generic "Series Ingester" would add too much complexity. The answer turned out to be no: `fetch_all(series_list, ...)` takes a list and loops. Adding or swapping a FRED series requires changing one list in `pipeline.py`, with no structural changes. The abstraction paid for itself immediately when PCU series were swapped in ADR-001.

**Consistency/Auditability vs. Performance — not yet fully resolved.**

F1 flagged the tension between storing every historical revision and query performance. F3 discovered this was the *biggest* unresolved risk (FRED revisions undermining point-in-time auditability). F4 addressed it with raw JSON archiving. But the deeper question — whether to use a proper append-only data store vs. timestamped flat files — was scoped away as out-of-MVP. The tension exists in the current architecture as an accepted limitation, not a solved problem.

**The surprise:** The weighting formula bug (Risk 7) was not a trade-off at all — it was a design document that didn't make it into code. The formula `S = w1(ΔIP) + w2(ΔCapUtil) - w3(ΔPPI) + w4(ΔInv)` was written correctly in F2 but implemented with equal positive weights. A characteristic assessment in F3 is what surfaced it. Architecture documents are not self-enforcing.

---

## 4. If You Started Over

**Three specific changes, each traceable to a concrete failure discovered later:**

1. **Archive raw FRED payloads in Filter 1, on day one.** The biggest architectural gap (Risk 4, ADR-007) was knowable from the problem statement: FRED revises data, and the system supports financial decisions. The auditability characteristic was identified in F1 as critical. But implementation settled for logging derived CSVs rather than raw JSON responses — a shortcut that required backfilling in F4. The fix was straightforward; delaying it was the mistake.

2. **Set the asymmetric PPI weight (`−1.0`) in the first working version of `transform.py`.** The formula was written correctly in F2's component spec. The implementation silently used equal positive weights. This produced plausible but analytically wrong output for the entire F3 milestone. The invariant "rising prices are a bad supply signal" should have been enforced the moment the weights dict parameter was created — not discovered during a risk audit.

3. **Add the validation filter before the S_score calculation in F3, not F4.** F2 explicitly specified a "Validation Filter gatekeeper that throws a fatal error if any upstream variable arrives as a raw number rather than a percentage." F3 identified its absence as Risk 9. F4 implemented it. A filter that was in the design document for two milestones before it was built is a gap that could have caused a silent Data Integrity failure during any F3 run.

