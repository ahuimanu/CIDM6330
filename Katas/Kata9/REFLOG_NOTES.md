# Kata9 — Git Reflog Recovery Exercise

## What we did

### 1. Made 3 commits

```
f7bc123  Kata9 reflog practice: dummy commit 3
720a99b  Kata9 reflog practice: dummy commit 2
37b0839  Kata9: add pipeline copy and integration tests
```

### 2. "Accidentally" nuked them

```bash
git reset --hard HEAD~3
# HEAD is now at 7e0f341  (the 3 Kata9 commits are gone from git log)
```

### 3. Used reflog to find the lost commits

```bash
git reflog --oneline -10
```

Output (relevant lines):

```
7e0f341 HEAD@{0}: reset: moving to HEAD~3          ← the reset itself
f7bc123 HEAD@{1}: commit: Kata9 reflog practice: dummy commit 3
720a99b HEAD@{2}: commit: Kata9 reflog practice: dummy commit 2
37b0839 HEAD@{3}: commit: Kata9: add pipeline copy and integration tests
```

`git reset --hard` only moves the branch pointer — it does **not** delete the
commits. They remain in the object store and show up in the reflog until Git's
garbage collector runs (default: 90 days).

### 4. Recovered by resetting to the last good hash

```bash
git reset --hard f7bc123
# HEAD is now at f7bc123  — all 3 commits restored
```

### Key takeaway

`git reflog` is a local-only safety net. Every time HEAD moves (commit, reset,
checkout, rebase, merge) Git records the old position. As long as you haven't
run `git gc --prune=now`, you can always get back to any recent state.
