# Foundation 1 — One-Page Rubric Grading Sheet
## Discover: Data + Architecture (CIDM 6330)

**Student:** Patrick Perez  
**Date:** 2026-03-01  
**Dataset / Agency:** FRED API / Federal Reserve Bank of St. Louis  
**PR Title:** Not provided in submitted Foundation1 artifacts  
**PR Link:** Not provided in submitted Foundation1 artifacts

---

## Gating Requirements (Pass/Fail)

- [x] Dataset is from **approved CIDM 6330 Dataset Pool**
- [ ] **Pull request** submitted to forked repo (deliverables included)
- [x] **AI_LOG.md** present and includes Foundation 1 entries
- [x] **Evidence of data access/retrieval** included (API response / screenshot / sample rows)

> Missing item: PR evidence (title/link/description) was not included in the Foundation1 submission artifacts reviewed here.

---

## Scoring (100 points total)

**Level key:** 4 = Exemplary · 3 = Proficient · 2 = Developing · 1 = Insufficient

| Category | Pts | Score | Level (1–4) | Notes (1–2 lines) |
|---|---:|---:|:---:|---|
| 1) Dataset Selection Justification | 25 | 24 | 4 | Strong dataset specificity, temporal detail, and rationale tied to semester viability. |
| 2) Initial Problem Space | 20 | 19 | 4 | Candidate problems are concrete and distinct; unknowns are explicit and decision-relevant. |
| 3) Architecture Characteristics Discovery (FSA Ch. 4–5) | 25 | 21 | 3 | Good characteristics and trade-off framing; could tighten mapping to explicit FSA terminology/quality attribute scenarios. |
| 4) AI Collaboration Log (AI_LOG.md) | 15 | 14 | 4 | Log clearly shows asks, outputs, adaptations, and judgment calls with rationale. |
| 5) Evidence, Professional Practice, Constraints | 10 | 8 | 3 | Evidence is present, but reproducibility and explicit peer-orthogonality handling need stronger proof. |
| 6) Repo / PR Quality & Submission Hygiene | 5 | 2 | 2 | Foundation docs are readable, but PR metadata/self-review evidence was not provided in artifacts. |
| **Total** | **100** | **88** |  | |

---

## Category Checklists (fast evaluator cues)

### 1) Dataset Selection Justification (25)
- [x] **Specific dataset** name (agency + exact dataset/table/endpoint/file)
- [x] **Access proof** (sample response / screenshot / sample rows)
- [x] **Relational depth:** ≥2 related tables/datasets + join keys explained
- [x] **Temporal:** update frequency + historical depth + granularity (with evidence)
- [x] **Why this dataset:** genuine interest + semester viability

### 2) Initial Problem Space (20)
- [x] **Domain observations** grounded in what they saw (examples)
- [x] **3–5 candidate problems** (concrete, distinct, testable)
- [x] **Unknowns/questions** that block choosing among problems (feasibility/value/scope)

### 3) Architecture Characteristics Discovery (25)
- [x] **5–7 characteristics** using correct FSA vocabulary
- [x] **Why each matters** tied to this dataset/domain (not generic)
- [x] **Tensions/trade-offs** identified and explained
- [x] **What’s unknown yet** stated (and why it’s unknown)

### 4) AI Collaboration Log (15)
- [x] What you asked
- [x] What you got
- [x] What you used/modified/rejected
- [x] Judgment calls (overrides/corrections + reasons)

### 5) Evidence / Constraints / Professional Practice (10)
- [x] Evidence over assertion throughout
- [ ] Orthogonality addressed if dataset overlaps peers
- [ ] Reproducible steps (links, queries, commands, paths)
- [x] No fabricated claims; uncertainty labeled

### 6) Repo / PR Hygiene (5)
- [x] Deliverables easy to locate; readable markdown
- [ ] Meaningful PR title + brief description
- [ ] Self-review confirmation included

---

## Written Feedback (for Drift)

**Strongest evidence of “touching the data”:**  
The CPI sample rows in `Foundation1/DATASET.md` plus accompanying FRED fetch/helper scripts demonstrate direct data retrieval and practical API interaction.

**Most promising candidate problem (and why):**  
Supply Chain “Shortage Scout” is strongest because it ties a clear business action (inventory strategy) to measurable leading indicators and a testable lag hypothesis.

**Biggest architectural tension you anticipate:**  
Auditability and data integrity versus implementation agility: tracking revisions/units rigorously increases complexity and may slow rapid iteration.

**One thing to validate before Foundation 2:**  
Define and test one explicit lag window assumption (e.g., `IPG3344S` lead time) with a reproducible query + notebook/script path.

**AI collaboration note (good judgment / concern):**  
Good judgment in documenting what was accepted vs. modified; continue this by showing one concrete AI suggestion you rejected with a brief technical reason.
