# Git & GitHub Course Quickstart (CLI-Only)

**Purpose:** This is the minimum operational guide students must follow on Day 1. It is intentionally short and prescriptive. All actions use **command-line git** and the **GitHub CLI (`gh`) only**.

---

## 0. Required Accounts & Tools

You must have:
- A GitHub account
- `git` installed and configured
- `gh` installed and authenticated (`gh auth login`)

Students are strongly encouraged to activate the **GitHub Student Developer Pack** for free access to professional tooling used in this course.

---

## 1. Fork and Clone the Assignment Repository

The instructor provides a repository in a private organization.

```bash
gh repo fork <org>/<repo> --clone
```

This creates:
- **upstream**: instructor-owned repo
- **origin**: your personal fork

Verify:
```bash
git remote -v
```

If `upstream` is missing:
```bash
git remote add upstream https://github.com/<org>/<repo>.git
```

---

## 2. Sync With Upstream

Before starting any work:

```bash
git checkout main
git pull upstream main
git push origin main
```

This keeps your fork aligned with the authoritative source.

---

## 3. Create a Feature Branch

```bash
git checkout -b feat/<short-topic>
```

All work happens on branches. Never work directly on `main`.

---

## 4. Work, Commit, Push

Edit files locally, then commit atomically:

```bash
git status
git add <files>
git commit -m "Describe the change clearly"
```

Push to your fork:

```bash
git push origin feat/<short-topic>
```

---

## 5. Open a Pull Request (CLI Only)

```bash
gh pr create --base <org>:main --head <username>:feat/<short-topic>
```

Follow prompts to link the Issue and describe the change.

---

## 6. Monitor and Update the PR

Check status:
```bash
gh pr status
gh pr checks
```

If changes are requested:
1. Update locally
2. Commit
3. Push again

The PR updates automatically.

---

## 7. Resolve Conflicts (If Required)

If conflicts occur:
- Resolve locally
- Run tests
- Continue or abort cleanly

Abort safely if needed:
```bash
git merge --abort
# or
git rebase --abort
```

---

## 8. Merge

When approved and checks pass:

```bash
gh pr merge
```

Delete the branch when prompted.

---

## 9. Receive Instructor Feedback

- Feedback is committed into your repository
- Rubrics are **GPG-encrypted** using your public key
- You decrypt feedback locally

This feedback becomes part of your repo history.

---

## One Rule to Remember

> If it didn’t go through a branch, a PR, and `gh`, it didn’t happen.
