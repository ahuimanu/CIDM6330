# Drift Consultation Log — Foundation 1: Discover
**Student:** Francis Kelechi Njoku
**Course:** CIDM 6330 — Software Architecture, Spring 2026
**Foundation Theme:** Discover — select a dataset, identify its characteristics, choose a storage approach

---

## Simulated Consultation Transcript

---

**Instructor:** Walk me through what Foundation 1 was asking you to do. Not what you built — why this foundation exists in the sequence.

**Student:** Foundation 1 is the Discover phase. Before you commit to an architecture, you have to understand the shape of your data. The katas forced me to look at two storage options — the filesystem (kata-01) and SQLite (kata-02) — so I had a concrete sense of what each one costs and what it gives you before I made any architectural choices in Foundation 2.

---

**Instructor:** What made you choose GDP data as your dataset?

**Student:** GDP data from the FRED API has properties that stress-test both storage approaches in interesting ways. It is time-series data, meaning every record has a date and a value, and the ordering of records matters — growth rates are computed by comparing adjacent rows. A flat file works fine for sequential reads, but if you want to ask "what was the growth rate in Q3 2019?", you need either a database index or a full scan. That tension between simple storage and query expressiveness is exactly what the foundation is designed to surface.

---

**Instructor:** You built a filesystem-based store in kata-01. What specifically did you give up by staying on the filesystem?

**Student:** Three things. First, there is no query capability — to find any record I have to read and scan the entire file. Second, concurrent writes are unsafe without an explicit locking layer. If two processes tried to append to the same file, records could get interleaved or corrupted. Third, there is no schema enforcement — a file accepts any bytes, so a malformed row is invisible until something downstream tries to parse it. What I gained was simplicity: no dependency, no setup, and the artifacts are human-readable, which matters a lot when you are still figuring out what shape the data should be.

---

**Instructor:** Then why move to SQLite in kata-02 instead of staying with the filesystem?

**Student:** Because the GDP data has a natural primary key — the date — and I needed to express that constraint in the storage layer, not in application code. With a file, the rule "no duplicate date" exists only as a comment or a convention. With SQLite I can write `date TEXT PRIMARY KEY` and the database enforces it for me. That is not just convenience; it is a correctness guarantee I can rely on in downstream stages. The schema also lets me add a `growth_rate` column that is nullable by design, which communicates intent: the first row has no previous row, so its growth rate is legitimately absent, not missing.

---

**Instructor:** What trade-off did SQLite introduce that the file approach did not have?

**Student:** Opacity. A `.db` file is binary — you cannot open it in a text editor and read what is inside. During development and debugging that is a real cost. I worked around it by generating a Markdown report alongside the database, but that report is a derived artifact; if the database and the report ever diverge, you have to trust the database and regenerate the report. The filesystem approach does not have that problem because the artifact is the data.

---

**Instructor:** If this were a production system receiving thousands of concurrent writes per second, would SQLite still be your choice?

**Student:** No. SQLite uses file-level locking, which means concurrent writers queue up. For a single-process batch pipeline processing quarterly GDP data it is perfectly adequate — there is no write concurrency because the pipeline runs once. But if I needed to ingest streaming data from multiple producers simultaneously, I would need a server-mode database like PostgreSQL that supports row-level locking and connection pooling. The insight from Foundation 1 is that SQLite is the right choice within its stated constraints, not unconditionally.

---

**Instructor:** Where did AI help you most in Foundation 1, and where did you push back?

**Student:** AI was most helpful in generating the schema DDL and the initial file I/O scaffolding quickly so I could focus on the architectural question rather than syntax. Where I pushed back was when AI suggested adding a second table for metadata in kata-02. That was premature — the assignment scope is a single series, single table, and adding metadata tables would have obscured the lesson. The lesson of kata-02 is not "use multiple tables"; it is "understand what a primary key constraint gives you." I kept the schema to one table intentionally.

---

**Instructor:** What would you change about your Foundation 1 work if you were doing it again?

**Student:** I would add a `--dry-run` flag to kata-01 earlier. I implemented it in kata-04's pipeline but the habit of "inspect without writing" is useful from the very first kata. It makes the code safer to run during experimentation, and it is a pattern that carries forward into every subsequent foundation. I would have introduced it as a discipline at kata-01 so it was automatic by the time the full pipeline arrived.

---

*Log completed: 2026-05-05*
*Foundation: 1 — Discover*
*Katas covered: kata-01 (filesystem), kata-02 (SQLite)*
