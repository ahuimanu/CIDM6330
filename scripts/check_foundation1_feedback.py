#!/usr/bin/env python3

import argparse
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request


def is_foundation1_feedback_markdown(path: str) -> bool:
    filename = path.rsplit("/", maxsplit=1)[-1]
    if not filename.lower().endswith(".md"):
        return False
    stem = filename[:-3].lower()
    compact = re.sub(r"[^a-z0-9]", "", stem)
    return "feedback" in compact and (
        "foundation1" in compact or ("foundation" in compact and "1" in compact)
    )


def github_get(url: str, token: str | None) -> dict | list:
    request = urllib.request.Request(url)
    request.add_header("Accept", "application/vnd.github+json")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request) as response:  # noqa: S310
        return json.load(response)


def list_org_repositories(org: str, token: str | None) -> list[dict]:
    repos: list[dict] = []
    page = 1
    while True:
        url = (
            f"https://api.github.com/orgs/{urllib.parse.quote(org)}/repos"
            f"?per_page=100&page={page}&type=all"
        )
        batch = github_get(url, token)
        if not batch:
            return repos
        repos.extend(batch)
        if len(batch) < 100:
            return repos
        page += 1


def repo_has_foundation1_feedback(org: str, repo: dict, token: str | None) -> bool:
    default_branch = repo["default_branch"]
    tree_url = (
        f"https://api.github.com/repos/{urllib.parse.quote(org)}/"
        f"{urllib.parse.quote(repo['name'])}/git/trees/"
        f"{urllib.parse.quote(default_branch)}?recursive=1"
    )
    tree = github_get(tree_url, token)
    for item in tree.get("tree", []):
        if item.get("type") == "blob" and is_foundation1_feedback_markdown(
            item.get("path", "")
        ):
            return True
    return False


def find_missing_repositories(org: str, token: str | None) -> list[str]:
    missing: list[str] = []
    for repo in list_org_repositories(org, token):
        if not repo_has_foundation1_feedback(org, repo, token):
            missing.append(repo["name"])
    return sorted(missing)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "List repositories in a GitHub organization that do not contain "
            "a Foundation 1 feedback markdown file."
        )
    )
    parser.add_argument("--org", default="WTAMU-CIDM6330")
    parser.add_argument("--token-env", default="GITHUB_TOKEN")
    args = parser.parse_args()

    token = os.getenv(args.token_env)
    try:
        missing = find_missing_repositories(args.org, token)
    except urllib.error.HTTPError as error:
        message = error.read().decode("utf-8", errors="replace")
        print(f"GitHub API request failed ({error.code}): {message}")
        return 1

    for repo_name in missing:
        print(repo_name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
