Kata6 Git Bisect Notes
======================

Summary
-------
Used `git bisect` inside the `CIDM6330` submodule to locate an intentional off-by-one bug introduced in `Katas/Kata6/kata6.py`.

Commands run
------------

```powershell
cd CIDM6330
git log --oneline -- Katas/Kata6
git bisect start
git bisect bad
git bisect good d415430
# For each checkout, run the test:
python Katas/Kata6/run_kata6.py
git bisect reset
```

Result
------
First-bad commit found:

82c8c1a6d589fd29f6b95b421e8e47618f166ded

Commit message: "Introduce intentional off-by-one bug for git-bisect exercise"

Diagnosis
---------
The bug was an intentional off-by-one change in `process_chunk()` that returned `sum(chunk) - 1` instead of `sum(chunk)`. This produced a total sum of `2000995` instead of `2001000` for the default run.

Notes
-----
- The bisect was performed in the `CIDM6330` submodule repository. After fixing or reverting the faulty commit, remember to update the parent repository to record the submodule pointer change.
