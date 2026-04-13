# Git — Bare Essentials (CLI‑Only)

This is a **minimal, markdown‑first guide** to Git. No theory detours. Just the commands you actually need day‑to‑day.

Preference assumed: **`git add -A`**.

---

## Mental model (lock this in)

* **Working tree** → your files on disk
* **Index (staging)** → what will go into the next commit
* **Commits** → immutable snapshots
* **Branches** → movable labels pointing at commits

> Git does not track files. It tracks **snapshots of content**.

---

## 0. One‑time setup

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

git config --global init.defaultBranch main
```

---

## 1. Create or clone a repository

### New repo

```bash
git init
```

### Clone existing repo

```bash
git clone https://github.com/owner/repo.git
cd repo
```

---

## 2. Check status (do this constantly)

```bash
git status
```

This answers three questions:

* What changed?
* What is staged?
* What is not staged?

---

## 3. Stage changes (your preferred way)

### Stage **everything** (adds, modifies, deletes)

```bash
git add -A
```

This means:

* New files → staged
* Modified files → staged
* Deleted files → staged

No surprises. No partial state.

---

## 4. Commit

```bash
git commit -m "Describe what changed"
```

**Example**

```bash
git commit -m "Add AIRAC dimension table"
```

A commit is:

> A snapshot + a message + a parent pointer

---

## 5. Create and switch branches

```bash
git checkout -b feature/my-change
```

Equivalent modern form:

```bash
git switch -c feature/my-change
```

---

## 6. Switch branches

```bash
git checkout main
```

Or:

```bash
git switch main
```

---

## 7. See commit history

```bash
git log --oneline --decorate --graph --all
```

This is the **only** log view you really need.

---

## 8. Undo mistakes (safe cases)

### Unstage everything (keep changes)

```bash
git reset
```

### Discard all local changes (danger)

```bash
git restore .
```

### Delete an unmerged branch

```bash
git branch -D feature/my-change
```

---

## 9. Sync with remote

### Pull latest changes

```bash
git pull
```

### Push current branch

```bash
git push
```

First push of a branch:

```bash
git push -u origin feature/my-change
```

---

## 10. Merge (local)

```bash
git checkout main
git pull
git merge feature/my-change
```

(You’ll usually do this via pull requests instead.)

---

## Absolute minimum daily workflow

```bash
git status
git add -A
git commit -m "message"
git push
```

If you can do just this reliably, you are already using Git **correctly**.

---

## What to ignore (for now)

You do **not** need immediately:

* Rebase mastery
* Interactive staging
* Cherry‑pick
* Submodules
* Bisect

Those are power tools. This is the cockpit checklist.

---

## Final rule

> If you’re confused, run `git status`.

It never lies.
