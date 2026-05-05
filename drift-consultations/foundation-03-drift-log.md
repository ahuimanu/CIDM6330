# Drift Consultation Log — Foundation 3: Develop
**Student:** Francis Kelechi Njoku
**Course:** CIDM 6330 — Software Architecture, Spring 2026
**Foundation Theme:** Develop — build MVP iterations, practice concurrency, document AI process

---

## Simulated Consultation Transcript

---

**Instructor:** Foundation 3 covers three distinct pieces: kata-05 (threading), kata-06 (multiprocessing), and the GDP pipeline. Why do you think the foundation groups these together?

**Student:** Because they all address the same underlying question from different angles: how do you make a pipeline faster when a single thread is not enough? Kata-05 explores I/O-bound concurrency, kata-06 explores CPU-bound concurrency, and the GDP pipeline puts both lessons into a real data acquisition context. By the end of Foundation 3 I should be able to look at a bottleneck and correctly identify whether it needs threads, processes, or is fast enough as-is.

---

**Instructor:** Kata-05 has two implementations — ThreadPoolExecutor and asyncio. What is the actual difference, and when does it matter?

**Student:** Both approaches let multiple fetch operations run concurrently instead of sequentially, but they work differently under the hood. `ThreadPoolExecutor` creates OS threads; each thread blocks on network I/O while others run. The GIL limits true parallelism for CPU work but does not block I/O waits, so threading works well here. `asyncio` is single-threaded but cooperative: each coroutine yields control when it would block on I/O, so the event loop runs other coroutines in the meantime. The practical difference shows up at scale. Threads have overhead per-thread — memory and context-switching cost — so at hundreds of concurrent requests, asyncio tends to scale better. For the small URL set in kata-05, the difference is measurable but not dramatic.

---

**Instructor:** You implemented a semaphore in the asyncio version. Why?

**Student:** Without a semaphore, `asyncio.gather()` fires all coroutines simultaneously. If the URL list has 100 items, that means 100 simultaneous open connections. Most servers and local network stacks have connection limits; exceeding them causes refused connections or timeouts that look like failures but are actually self-inflicted throttling. The semaphore limits concurrency to a configured number — say 10 — so connections open and close in controlled batches rather than all at once.

---

**Instructor:** What trade-off does the semaphore introduce?

**Student:** It adds a bottleneck. With the semaphore at 10, the 11th request waits for one of the first 10 to finish. Without it, all 11 could start at once. For a URL set small enough that the server can handle it, the semaphore slows things down unnecessarily. I set the limit via configuration so it can be tuned rather than hardcoded, which keeps the trade-off adjustable without changing the code.

---

**Instructor:** Kata-05 uses a threading lock for thread-safe writes. What specifically does it protect?

**Student:** It protects the shared `results` and `errors` dictionaries. Without the lock, two threads completing at the same time could both attempt to write to the same dictionary simultaneously. In CPython this is unlikely to corrupt the dictionary due to the GIL, but the GIL is an implementation detail, not a contract — it can be released at any point between bytecode instructions. The lock makes the safety explicit and does not rely on GIL behavior, which makes the code correct by construction rather than correct by coincidence.

---

**Instructor:** Now kata-06. You used `ProcessPoolExecutor` instead of `ThreadPoolExecutor`. Why?

**Student:** Because the work is CPU-bound. Each chunk computes statistics including prime counts, which requires arithmetic on every number in the range. The GIL prevents two threads from executing Python bytecode simultaneously, so threading would not actually achieve parallelism for this work — threads would take turns. Processes bypass the GIL entirely because each process has its own Python interpreter and memory space. The cost is higher: spawning processes is slower than spawning threads, and data must be serialized (pickled) to pass between processes. For CPU-bound work that runs for seconds, that cost is worth it.

---

**Instructor:** The kata-06 README documents a git bisect exercise. Walk me through what bisect does and why it was in this kata.

**Student:** `git bisect` does a binary search through commit history to find the commit that introduced a bug. You give it a known-good commit and a known-bad commit, and it checks out the midpoint. You test it, mark it good or bad, and bisect halves the range again. For a 100-commit history it finds the bug in at most 7 steps instead of 100. The kata included an intentional `total_count` aggregation bug — it was summing counts incorrectly across chunks — and the exercise required using bisect to locate the exact commit where the bug appeared. The lesson is that knowing git history is a debugging tool, not just an audit trail.

---

**Instructor:** The GDP pipeline in Foundation 3 uses a sample payload by default. Why not always call the live FRED API?

**Student:** Two reasons. First, reproducibility: tests and local runs should not depend on network access or a valid API key. A missing key would make the code unrunnable for anyone without a FRED account, which includes automated grading. Second, the assignment is about the pipeline architecture, not about API credential management. Using sample data by default means the pipeline always produces the same output for the same input, which makes it testable and demonstrable without any external dependency.

---

**Instructor:** The acquire module has a fallback from live to sample on error. Is that always the right behavior?

**Student:** No — it depends on whether a stale result is worse than no result. For a research pipeline displaying GDP trends, falling back to sample data silently would be dangerous: the report would look current but would actually contain hardcoded 2020 values. A user who did not know about the fallback could draw wrong conclusions. In a production context I would make the fallback opt-in and log a clear warning when it activates. In this MVP the fallback exists for developer convenience, and the configuration flag `FRED_FALLBACK_TO_SAMPLE_ON_ERROR` makes it explicit and controllable.

---

**Instructor:** The pipeline keeps raw JSON files and transformed JSON files in separate directories. Why not merge them?

**Student:** Because the transformation step may discard or modify data, and you want to be able to re-run the transformation with different logic without re-fetching from the API. If raw and transformed were merged into one file, a bug in the transformation would corrupt the only copy of the source data. Keeping them separate means I can always recover by re-running the transform stage against the raw file. It also makes the pipeline stages independently inspectable — I can verify that acquisition produced the expected raw payload before checking whether the transformation is correct.

---

**Instructor:** Where did AI fall short in Foundation 3?

**Student:** AI-generated documentation in Foundation 3 was consistently too generic. It wrote descriptions that could apply to any pipeline rather than describing the specific modules, outputs, and limitations of this GDP pipeline. I rewrote the README from scratch to reference the actual module names, the real output filenames, and the specific current limitations — like the absence of a dedicated CLI and the deferred database output. Generic documentation is worse than no documentation because it creates a false sense that things are explained when they are not.

---

*Log completed: 2026-05-05*
*Foundation: 3 — Develop*
*Katas covered: kata-05 (ThreadPoolExecutor and asyncio, semaphore, thread-safe writes), kata-06 (ProcessPoolExecutor, CPU-bound work, git bisect), GDP pipeline (acquire, transform, report, config, logging)*
