# GitHub CLI Pull Requests (CLI‑Only)

This is a **minimal, markdown-first tutorial** for creating and managing pull requests using **only** the GitHub CLI (`gh`) and `git`. No UI required.

---

## 0. One‑time setup

Install and authenticate:

```bash
# macOS
brew install gh

# Windows
winget install GitHub.cli

# authenticate
gh auth login
gh auth status
```

---

## 1. Clone a repository

```bash
gh repo clone owner/repo
cd repo
```

**Example**

```bash
gh repo clone your-org/airlineops
cd airlineops
```

---

## 2. Create a feature branch

Always work on a branch.

```bash
git checkout -b feature/my-change
```

**Example**

```bash
git checkout -b feature/add-airac-index
```

---

## 3. Make changes and commit

```bash
git status
git add .
git commit -m "Describe the change clearly"
```

**Example**

```bash
git add warehouse/airac.py
git commit -m "Add AIRAC index computation"
```

---

## 4. Push the branch

First push sets upstream tracking.

```bash
git push -u origin feature/my-change
```

After this, `git push` is sufficient.

---

## 5. Create the pull request

### Interactive (recommended)

```bash
gh pr create
```

You’ll be prompted for:

* Base branch (usually `main`)
* Title
* Body
* Whether to push the branch

### Non‑interactive

```bash
gh pr create \
  --base main \
  --head feature/my-change \
  --title "Add AIRAC index" \
  --body "Computes and persists AIRAC index for warehouse pipeline"
```

---

## 6. View the pull request

```bash
gh pr view
```

With comments:

```bash
gh pr view --comments
```

Open in browser (still CLI‑initiated):

```bash
gh pr view --web
```

---

## 7. Update an existing PR

Make more commits on the same branch:

```bash
git add .
git commit -m "Fix edge case in AIRAC rollover"
git push
```

The pull request updates automatically.

---

## 8. Check out a PR locally

```bash
gh pr checkout <PR_NUMBER>
```

**Example**

```bash
gh pr checkout 42
```

---

## 9. Merge the pull request

```bash
gh pr merge
```

Common strategies:

```bash
gh pr merge --squash
gh pr merge --rebase
gh pr merge --merge
```

(Repository rules may restrict options.)

---

## 10. Clean up after merge

```bash
git checkout main
git pull
git branch -d feature/my-change
git push origin --delete feature/my-change
```

---

## Minimal mental model

* **Git** creates commits
* **Branches** hold work
* **Pull requests** ask GitHub to merge one branch into another
* **`gh`** is just the wiring

> A pull request is simply: “Please merge **this branch** into **that branch**.”

---

## Absolute minimum cheat sheet

```bash
gh repo clone owner/repo
cd repo
git checkout -b feature/x
git commit -am "change"
git push -u origin feature/x
gh pr create
gh pr merge
```
