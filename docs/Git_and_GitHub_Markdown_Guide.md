# Markdown Guide: Suggested Git + GitHub Practices

Use this as a reference for day-to-day Git work, GitHub collaboration, and long-lived repo health.

---

## Repository foundations

### Prefer a predictable repo layout

* Put docs in `docs/`, runbooks in `docs/runbooks/`, ADRs in `docs/adr/`, architecture diagrams in `docs/architecture/`.
* Keep scripts in `scripts/` and keep them composable and documented.
* Keep configuration minimal and centralized (`pyproject.toml`, `.editorconfig`, `.gitignore`, `.gitattributes`).

### Always include these repo files

* `README.md` (what, why, how, quickstart)
* `LICENSE` (explicitly)
* `CONTRIBUTING.md` (how to contribute, local setup, PR rules)
* `CODE_OF_CONDUCT.md` (if multi-contributor/community-facing)
* `SECURITY.md` (vuln reporting path)
* `.editorconfig` (consistent whitespace/endings across editors)
* `.gitignore` tuned to your stack
* `.gitattributes` to prevent diff noise and enforce text handling

---

## Branching model (pick one and enforce it)

### Trunk-based development (recommended for most teams)

* `main` is always releasable.
* Short-lived branches: `feat/*`, `fix/*`, `chore/*`, `docs/*`.
* Merge via PR with CI required.
* Prefer feature flags over long-lived branches.

### GitFlow (only if you truly need parallel release trains)

* More moving parts: `develop`, `release/*`, `hotfix/*`.
* Costs real coordination overhead—avoid by default.

**Rule:** whichever model you choose, codify it in `CONTRIBUTING.md` and enforce via branch protections.

---

## Commit standards

### Commit content rules

* One logical change per commit.
* Keep commits buildable whenever possible (especially on trunk).
* Avoid drive-by refactors mixed with behavior change unless tightly related.

### Conventional Commits (strongly recommended)

Use:

* `feat:` new capability
* `fix:` bug fix
* `docs:` documentation only
* `refactor:` non-functional change
* `test:` tests only
* `perf:` performance improvement
* `build:` build/deps tooling
* `ci:` CI config changes
* `chore:` maintenance

Examples:

* `feat(cli): add manifest reconcile subcommand`
* `fix(ingest): handle missing carrier decode rows`
* `refactor(db): isolate sql builders`

### Write commit messages like an audit log

* Imperative mood: “Add”, “Fix”, “Remove”.
* Explain *why* when non-obvious.
* If a change has risk: note it in the body and how it’s mitigated.

---

## Pull request (PR) standards

### PR size and shape

* Prefer small PRs: easy review, low merge risk.
* If big changes are unavoidable: split into stacked PRs or “mechanical refactor” PR + “behavior change” PR.

### PR description template (high-signal)

Include:

* **Context:** why now?
* **What changed:** concise bullets
* **How to test:** exact commands / steps
* **Risk:** what could break?
* **Screenshots/logs:** when relevant
* **Follow-ups:** explicitly listed (not implicit)

### Review etiquette that scales

* Review the architecture first, then code style.
* Ask for clarity on invariants, edge cases, failure modes.
* Prefer “request changes” only for correctness/safety/maintainability—not preferences.

---

## GitHub workflows & protections

### Branch protection rules (baseline)

* Require PRs for `main`.
* Require status checks to pass (CI).
* Require at least 1–2 approvals (assuming team work).
* Require “conversation resolved”.
* Require linear history (optional but helps cleanliness).
* Restrict force-push on protected branches.
* Require signed commits if your org does that.
* Require CODEOWNERS review for sensitive areas.

### CODEOWNERS (use it)

* Put it in `.github/CODEOWNERS`.
* Assign ownership for core modules, infra, security-sensitive paths.

### Issues and milestones

* Use Issues for work tracking; PRs reference Issues.
* Use Milestones for releases/epochs.
* Label taxonomy (minimal but consistent): `bug`, `enhancement`, `docs`, `security`, `tech-debt`, `blocked`.

---

## CI/CD and quality gates

### CI principles

* Fast feedback first: lint + unit tests early.
* Cache dependencies/build artifacts.
* Run PR checks on every push; run heavier checks nightly or on merge.

### Required CI checks (typical “gold baseline”)

* Lint/format
* Typecheck (if applicable)
* Unit tests
* Security scanning (dependency + code scanning)
* Build/package check
* (Optional) Integration tests for critical paths

### Release discipline

* Tag releases (`vX.Y.Z` semver) and generate release notes.
* Automate changelogs when possible.
* Prefer reproducible builds; pin dependencies.

---

## Security and supply chain

### Secrets

* Never commit secrets.
* Use GitHub Actions secrets, OIDC, or a vault.
* Add secret scanning.

### Dependencies

* Enable Dependabot (updates + security alerts).
* Pin direct dependencies; control transitive drift.
* Review license compatibility for deps.

### Signed commits/tags (when you need high assurance)

* Use GPG or SSH signing.
* Enforce in branch rules if your org policy requires it.

---

## Docs and architecture records

### ADRs (Architecture Decision Records)

* Record decisions, not narratives.
* Each ADR should include: context, decision, alternatives, consequences, and status.
* Keep them immutable once “Accepted”; supersede with a new ADR.

### READMEs that actually work

* Top: what it is, who it’s for, and one command to run.
* Include troubleshooting and a “common tasks” section.
* Keep “design philosophy” separate from “how to run”.

---

## Git hygiene: commands and habits

### Don’t rewrite shared history

* If it’s on `main` (or another protected branch), no rebases/force pushes.
* If it’s your local branch: clean history is fine (interactive rebase) **before** PR review starts.

### Use rebase vs merge intentionally

* **Rebase** local work onto updated `main` to resolve conflicts early.
* **Squash merge** to keep history clean (common on GitHub).
* **Merge commit** only if you value full branch history.

### Keep your working tree safe

* Commit frequently (logical steps).
* Use `git stash` sparingly; prefer WIP commits on a personal branch if needed.
* Use `git bisect` for regression hunting when you can reproduce.

---

## Markdown specifics for GitHub

### Headings and structure

* One `#` per page, then `##`, `###`.
* Keep headings descriptive and scannable.
* Prefer short paragraphs + bullets.

### Code blocks

* Always specify language:

  ```bash
  git status
  ```

* For config: `yaml`, `toml`, `json`, `ini`.
* For diffs:

  ```diff
  - old
  + new
  ```

### Links and references

* Use relative links within repo: `docs/runbooks/deploy.md`
* Reference issues/PRs by `#123`.
* Cross-link ADRs and docs from PRs.

### Tables (use sparingly)

* Tables are good for matrices, bad for prose.
* Keep cells short.

### Task lists for PR checklists

* Use GitHub-flavored task lists:

  * [ ] Tests added
  * [ ] Docs updated
  * [ ] Migration notes included

### Collapsible sections for long logs

````md
<details>
<summary>CI log excerpt</summary>

```text
...log...
````

</details>
```

---

## High-leverage GitHub features

### Actions

* Use reusable workflows (`workflow_call`) for standard pipelines.
* Lock down permissions (least privilege).
* Prefer OIDC over long-lived cloud keys.

### Environments

* Require approvals for prod deploy environments.
* Store environment-specific secrets there.

### Projects (optional)

* Use GitHub Projects for cross-repo planning if your org actually maintains it.

---

## Typical daily workflow (Git + GitHub CLI)

This is a “gold path” workflow that keeps history clean, reviews fast, and CI reliable.

### 0) One-time setup (per machine)

```bash
# Git identity
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# Helpful defaults
git config --global init.defaultBranch main
git config --global pull.rebase true

# GitHub CLI auth
gh auth login

# (Optional) set default repo protocol
gh config set git_protocol ssh
```

### 1) Sync `main`

```bash
git checkout main
git fetch origin
git pull --ff-only
```

### 2) Create a focused branch

```bash
# choose a consistent prefix
git checkout -b feat/short-slug
# or
# git checkout -b fix/short-slug
# git checkout -b chore/short-slug
```

### 3) Work in small commits

```bash
# see what changed
git status

git add -p

git commit -m "feat(scope): concise intent"

# repeat as needed
```

### 4) Rebase on latest `main` before pushing (avoid surprise conflicts)

```bash
git fetch origin
git rebase origin/main

# if conflicts, fix files, then:
# git add <files>
# git rebase --continue
```

### 5) Push branch to origin

```bash
git push -u origin HEAD
```

### 6) Open a PR with `gh`

```bash
# Create PR (interactive prompts are fine)
gh pr create --fill

# Or specify title/body explicitly
# gh pr create --title "..." --body "..." --base main

# View PR in browser
gh pr view --web
```

### 7) Monitor CI and reviews

```bash
# Watch CI checks and review activity
gh pr checks --watch

# See review status and comments
gh pr view
```

### 8) Respond to review; push updates

```bash
# make fixes, then
git add -p
git commit -m "fix(scope): address review comments"

git push
```

### 9) Merge (choose your policy)

Pick one approach and standardize it repo-wide.

```bash
# Squash merge (common default)
gh pr merge --squash --delete-branch

# Rebase merge (keeps individual commits)
# gh pr merge --rebase --delete-branch

# Merge commit (keeps branch structure)
# gh pr merge --merge --delete-branch
```

### 10) Post-merge cleanup locally

```bash
git checkout main
git pull --ff-only

git branch -d feat/short-slug

# prune deleted remote branches
git fetch --prune
```

---

## Release workflow (typical)

### Tagging and GitHub releases

```bash
# Update main
git checkout main
git pull --ff-only

# Create an annotated tag
# (choose semver versioning)
git tag -a v1.2.3 -m "Release v1.2.3"

git push origin v1.2.3

# Create GitHub release with generated notes
# (requires tag present)
gh release create v1.2.3 --generate-notes

# View releases
# gh release list
```

---

## Emergency fix workflow (hotfix)

### If `main` is broken in production

```bash
# branch from main
git checkout main
git pull --ff-only

git checkout -b hotfix/short-slug

# fix + commit
git add -p
git commit -m "fix: stop production crash on startup"

git push -u origin HEAD

# open PR
gh pr create --fill

gh pr checks --watch

# merge (fast)
gh pr merge --squash --delete-branch
```

---

## “Gold standard” checklist (printable)

* [ ] `main` protected + required checks
* [ ] Clear branching model documented
* [ ] Conventional commits (or equivalent) enforced culturally
* [ ] PR template + high-signal descriptions
* [ ] CI: lint/type/test/security/build
* [ ] Dependabot + secret scanning enabled
* [ ] CODEOWNERS for critical paths
* [ ] ADRs for major decisions
* [ ] Releases tagged + notes generated
* [ ] Docs are navigable and current
