# Kata6 — Concurrency + Git Bisect Exercise

This kata demonstrates processing a large dataset in parallel using multiple processes.

Run:

```bash
python CIDM6330/Katas/Kata6/run_kata6.py
```

Overview:
- `kata6.py`: main implementation (chunking, ProcessPoolExecutor, retry on failure)
- `run_kata6.py`: small runner for quick local runs

Git tasks:
- Make an initial commit after adding the scaffold files.
- Introduce an intentional bug in a later commit (see Kata6 exercise description).
- Use `git bisect` to find the commit that introduced the bug.
