# GitHub Repository Settings Checklist (Course Enforced)

**Purpose:** These settings mechanically enforce the course handbook. Students are not expected to change these. Instructors must ensure they are enabled.

---

## 1. Branch Protection (main)

Enable branch protection rules on `main`:

- ☐ Require a pull request before merging
- ☐ Require approvals (≥1)
- ☐ Dismiss stale approvals when new commits are pushed
- ☐ Require status checks to pass before merging
- ☐ Require branches to be up to date before merging
- ☐ Include administrators

These settings prevent bypassing review and CI.

---

## 2. Merge Strategy

Select **one** merge method:

- ☐ Allow squash merging (RECOMMENDED)
- ☐ Disable merge commits
- ☐ Disable rebase merging (unless explicitly teaching it)

Optionally:
- ☐ Require linear history

Consistency is more important than preference.

---

## 3. Pull Request Defaults

- ☐ Default PR base branch: `main`
- ☐ Require conversation resolution before merging
- ☐ Enable auto-delete of head branches after merge

---

## 4. Issues Configuration

- ☐ Issues enabled
- ☐ Issue templates provided (optional but recommended)
- ☐ Labels enabled for triage (e.g., `bug`, `enhancement`, `docs`)

Issues are the authoritative unit of intent.

---

## 5. Actions / CI

- ☐ GitHub Actions enabled
- ☐ Required workflows configured as status checks
- ☐ Failing workflows block merges

CI provides mechanical evidence of correctness.

---

## 6. Security & Integrity

- ☐ Dependency graph enabled
- ☐ Dependabot alerts enabled
- ☐ Secret scanning enabled

These are baseline platform protections.

---

## 7. Access Control

- ☐ Students: write access to forks only
- ☐ Instructor/TAs: review + admin on upstream

Prevents accidental or intentional bypass of workflow.

---

## 8. CLI Compatibility

Ensure nothing in repo policy requires web-only interaction:

- PRs can be created via `gh`
- Reviews visible via `gh`
- Merges executable via `gh`

CLI-first is a course requirement.

---

## Final Assertion

> If a rule matters, it must be enforced by GitHub settings—not memory or goodwill.

