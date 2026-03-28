Python Focus: Concurrency (Multiprocessing)
Git Focus: Git Bisect
The Exercise:

Create a data processing script that:

Reads a large dataset (or simulates one with generated data)
Splits the data into chunks
Processes each chunk in a separate process using multiprocessing
Combines results from all processes into a final output
Requirements:

Use multiprocessing.Pool or concurrent.futures.ProcessPoolExecutor
Implement CPU-bound processing (e.g., statistical calculations, data aggregation)
Handle the case where a worker process fails
Add progress reporting (how many chunks completed)
Git Tasks:

Intentionally introduce a bug in one of your commits (or use an existing project with a known bug)
Use git bisect to find the commit that introduced the bug:
git bisect start
git bisect bad  # current commit is broken
git bisect good <known-good-commit>
# Git checks out middle commit; test and mark good/bad
Document the bisect process and what you found
Stretch:

Implement shared state between processes using multiprocessing.Manager