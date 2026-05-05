# Drift Consultation Log — Foundation 2: Define
**Student:** Francis Kelechi Njoku
**Course:** CIDM 6330 — Software Architecture, Spring 2026
**Foundation Theme:** Define — commit to a problem, consume an external API, build a data transformation pipeline

---

## Simulated Consultation Transcript

---

**Instructor:** Foundation 2 is called Define. What were you defining, and why does that matter before you build anything?

**Student:** I was defining the architecture of the data flow — how raw data moves from an external source into a usable local store. Kata-03 locked in the acquisition contract: the system talks to the FRED API, handles pagination, and survives network failures. Kata-04 locked in the transformation contract: raw CSV becomes typed, validated rows in SQLite, and a Markdown report is the human-readable output. Once both contracts are defined, later foundations can build on them without revisiting these questions.

---

**Instructor:** Talk me through the retry logic in kata-03. Why exponential backoff specifically?

**Student:** The FRED API can respond with transient errors — 429 (rate limit), 502, 503, 504 (upstream issues). A naive retry immediately re-fires the request, which either hammers a rate-limited server faster or hits the same upstream failure again. Exponential backoff spaces the retries geometrically: attempt 0 waits 0.75 seconds, attempt 1 waits about 1.3 seconds, attempt 2 about 2.3 seconds, and so on up to a 25-second cap. The jitter — a random offset between 5% and 30% of the sleep — prevents the "thundering herd" problem where many clients retry in lockstep after a shared outage and all hammer the server at the same instant.

---

**Instructor:** What did you give up with that retry design?

**Student:** Latency predictability. If a request fails, the caller cannot know how long the retry loop will take — it depends on how many attempts fail and what the random jitter lands on. For an interactive application that would be unacceptable. For a batch pipeline that runs quarterly and saves results to a file, unpredictable retry latency is a fine trade for reliability. I accepted that trade explicitly because this is an offline pipeline, not a real-time service.

---

**Instructor:** The retry function caps retries at 5 and uses `raise RuntimeError` at the end. Why not just return an empty list?

**Student:** Because an empty list is a valid successful result — a series with no observations would legitimately return zero rows. If I returned an empty list on failure, the caller would have no way to distinguish "FRED returned no data" from "the request failed after five retries." Raising an exception makes the failure mode explicit and stops the pipeline immediately instead of writing an empty file to disk and pretending the run succeeded. Silent failures are harder to diagnose than loud ones.

---

**Instructor:** Kata-04 has a `--dry-run` flag. Walk me through why that exists.

**Student:** The pipeline is destructive in the sense that it overwrites the database and report on every run. During development I needed a way to check that the CSV would parse correctly and that the row count looked right without committing any changes to disk. The dry-run path reads and validates the input, prints a summary of what would happen, and exits without touching the database, log, or report. That separation between "inspect" and "write" is especially useful in CI — I can run the dry-run in a test without needing a writable filesystem or a pre-seeded database.

---

**Instructor:** The `load_rows` function uses `INSERT OR REPLACE`. What does that buy you, and what does it risk?

**Student:** It buys idempotency. If I run the pipeline twice on the same CSV, the second run does not double the row count — it replaces existing rows by primary key (date). That makes the pipeline safe to re-run after a partial failure. The risk is silent data mutation: if the source CSV is corrected and a row's value changes, `INSERT OR REPLACE` will silently update it without any record that the change happened. For an audit-sensitive system I would want a separate update log. For this pipeline, which processes public GDP data that rarely gets revised, the trade-off is acceptable.

---

**Instructor:** `compute_growth_rates` fetches all rows into Python, computes growth rates, and then runs a batch UPDATE. Why not do it in a single SQL query?

**Student:** I considered a window function approach using `LAG()`, but SQLite's support for window functions depends on the version. The version check would have added complexity that was not justified by the assignment scope. The Python approach is explicit and easy to follow: fetch the rows in date order, iterate with a running `prev_value`, compute the rate, batch the updates. For a dataset of a few hundred quarterly observations the performance difference is negligible. If this were millions of rows, I would revisit that decision and accept the SQL complexity in exchange for eliminating the Python round-trip.

---

**Instructor:** The `GdpRow` dataclass is `frozen=True`. Why frozen?

**Student:** Because a row read from a CSV should not change during the pipeline. `frozen=True` makes the dataclass hashable and prevents accidental mutation — if any downstream code tried to write `row.value = something`, Python would raise a `FrozenInstanceError` immediately instead of silently corrupting data. It is a cheap invariant: one keyword, zero runtime cost, immediate failure on violation.

---

**Instructor:** Where did AI help in Foundation 2 and where did you override it?

**Student:** AI generated the initial retry loop and the schema SQL quickly, which let me spend time on the harder question of pipeline structure rather than boilerplate. I overrode AI twice. First, AI suggested using `requests.Session` for connection reuse across retries. That was technically correct but added state to what should be a stateless function, and the kata scope did not involve enough requests to make connection reuse measurable. Second, AI suggested storing the raw JSON from FRED directly in SQLite as a BLOB column. I rejected that because it mixes raw and transformed storage in a single table, which makes the transformation step invisible. Keeping raw JSON in files and transformed rows in SQLite preserves the boundary between stages.

---

**Instructor:** If the CSV format changed — say, column names were renamed — where would kata-04 break and how quickly would you find it?

**Student:** It would break in `extract_rows`, which uses `csv.DictReader` and accesses `row.get("date")` and `row.get("value")` by name. The `get` calls return `None` for missing keys, which then fails the `not date` check in `validate_and_transform`. The row would be logged as invalid with the actual content visible in the validation log. So the pipeline would not crash — it would produce an empty database and a log full of `[INVALID]` entries. That is a fast, visible failure: the report shows zero rows and the log shows why.

---

*Log completed: 2026-05-05*
*Foundation: 2 — Define*
*Katas covered: kata-03 (API consumption, FRED, pagination, retry), kata-04 (data transformation pipeline, SQLite, growth rates, report)*
