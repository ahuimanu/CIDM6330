# Git & GitHub Operations Handbook

## Canonical, Non‑Negotiable Baseline for Graduate Systems Development

This handbook defines **required operating behavior** for all course repositories. It is intentionally conservative and grounded in primary sources (Git and GitHub documentation). These rules are **not open for negotiation**. They exist to standardize collaboration, reduce ambiguity, and allow assessment to focus on systems thinking rather than workflow variance.

---

## 0. GitHub Student Developer Pack (Required Context)

Students are **strongly encouraged** to activate the GitHub Student Developer Pack early in the course.

The Student Developer Pack provides free access to professional-grade development tools that would otherwise be cost-prohibitive. In this course, it serves a structural purpose:

- removes financial friction
- legitimizes industry tooling usage
- reinforces GitHub as a *platform*, not just a repository host

Activation is expected by the end of the first two weeks of the course. No grading penalty is attached, but students who delay activation may be unable to fully participate in later tooling workflows.

---

## 1. Foundational Principle

### 1.1 The repository *is* the system

A GitHub repository is simultaneously:

- a change‑control system (Git)
- a collaboration system (Issues, Pull Requests)
- a governance system (branch protection, required checks)
- an evidence system (history, reviews, CI results)

All course work is evaluated **through the behavior of this system**.

---

## 2. Non‑Negotiable Laws

### LAW 1 — `main` is protected

- No direct commits to `main`.
- All changes enter via Pull Requests.
- Branch protection rules enforce this.

### LAW 2 — Every meaningful change has an Issue

- Any non‑trivial work must be associated with an Issue.
- Issues define **intent**; PRs define **change**.

### LAW 3 — Every change is reviewed

- No self‑merging of substantive work.
- Reviews are required before merge.

### LAW 4 — CI must pass before merge

- Required checks must be green.
- Local success is not evidence.

### LAW 5 — Merge behavior is standardized

- The repository specifies **one** merge method (typically squash merge).
- This is enforced via GitHub settings.

---

## 3. Branching Rules

### 3.1 Branch creation

All work occurs on branches created from `main`.

Required naming:

- `feat/<short-description>`
- `fix/<short-description>`
- `chore/<short-description>`

### 3.2 Branch lifespan

- Branches are short‑lived.
- Branches are deleted after merge.

---

## 4. Commit Discipline

### 4.1 Atomic commits

Each commit represents **one coherent change**.

### 4.2 Meaningful commit messages

Commit messages must describe *what changed* clearly.

### 4.3 No rewriting shared history

Once a branch is pushed and under review, do not rebase or amend unless explicitly instructed.

---

## 5. Issues: Unit of Intent

- Issues define the problem and expected outcome.
- Issues are managed via the GitHub CLI.

Required familiarity:

- `gh issue create`
- `gh issue list`
- `gh issue status`

---

## 6. Pull Requests: Unit of Change

### 6.1 PRs are mandatory

All changes enter via PRs.

### 6.2 PR quality expectations

- One issue per PR
- Reviewable scope
- Relevant changes only

### 6.3 PR lifecycle via CLI

- Create: `gh pr create`
- Inspect: `gh pr status`
- Validate: `gh pr checks`
- Merge: `gh pr merge`

---

## 7. Merge Conflicts: Standard Procedure

### 7.1 Conflict types

- Merge conflicts (`git merge`)
- Rebase conflicts (`git rebase`)

### 7.2 Required handling

1. Inspect conflict markers
2. Resolve locally
3. Run tests
4. Stage resolved files
5. Continue or abort cleanly

Abort commands:

- `git merge --abort`
- `git rebase --abort`

---

## 8. Governance via Platform

- Branch protection enforces policy
- Required reviews and checks eliminate ambiguity
- The platform is the enforcer, not personal judgment

Early GovZero alignment:

- Intent → Issue
- Change → PR
- Evidence → CI + review
- Attestation (later) → observed behavior

---

## 9. CLI‑First Expectation

Students are expected to operate using:

- command‑line `git` for local history and conflicts
- `gh` for all GitHub operations

Web UI usage is discouraged for core workflows.

---

## 10. Canonical Student Workflow (CLI‑Only)

### 10.1 Initial setup

The instructor provides a **source repository** in a private organization.

Student workflow:

1. Fork the repository into their own GitHub account:

   ```bash
   gh repo fork <org>/<repo> --clone
   ```

2. This creates:
   - an upstream repo (instructor)
   - a personal fork (student)

### 10.2 Configure remotes

Verify remotes:

```
git remote -v
```

Expected:

- `origin` → student fork
- `upstream` → instructor repo

If missing:

```
git remote add upstream https://github.com/<org>/<repo>.git
```

### 10.3 Local development loop

1. Sync from upstream:

   ```bash
   git checkout main
   git pull upstream main
   ```

2. Create a feature branch:

   ```bash
   git checkout -b feat/<topic>
   ```

3. Work locally, commit atomically
4. Push to personal fork:

   ```bash
   git push origin feat/<topic>
   ```

### 10.4 Open a Pull Request

Create PR via CLI:

```bash
gh pr create --base <org>:main --head <username>:feat/<topic>
```

Check status:

```bash
gh pr status
gh pr checks
```

Iterate locally → push updates → PR updates automatically.

### 10.5 Merge

When approved and checks pass:

```bash
gh pr merge
```

---

## 11. Instructor Feedback via GPG‑Encrypted Rubrics

### 11.1 Feedback delivery model

- Instructor feedback is committed **into the student fork**.
- Feedback files are **GPG‑encrypted** using the student’s public key.

### 11.2 Student responsibility

- Students must provide a valid GPG public key.
- Students are responsible for decrypting feedback locally.

### 11.3 Feedback artifacts

- Encrypted rubric files are committed as normal Git artifacts.
- Feedback appears as part of repo history and PR discussion context.

This ensures:

- confidentiality
- auditability
- reproducibility of evaluation

---

## 12. What This Handbook Is Not

- Not a debate about Git philosophy
- Not optimized for solo hacking
- Not tolerant of workflow improvisation

It **is** optimized for shared systems, traceability, and professional discipline.

---

## 13. One‑Sentence Summary

> All work flows through Issues and Pull Requests, enforced by GitHub, operated from the CLI, with conflicts resolved deliberately and feedback delivered as auditable artifacts.
