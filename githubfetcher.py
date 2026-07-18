

from __future__ import annotations

import os
import time
import logging
from typing import Optional

from github import Github, Auth
from github.GithubException import (
    UnknownObjectException,
    RateLimitExceededException,
    BadCredentialsException,
    GithubException,
)

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger("github_fetcher")

# Cap so we never build a multi-megabyte prompt from a monster PR.
MAX_FILES_TO_INCLUDE = 50
MAX_PATCH_CHARS_PER_FILE = 6000  # truncate individual huge patches

BINARY_PLACEHOLDER = "[Binary or non-diffable file — content not shown]"


class GitHubFetchError(Exception):
    """Raised for any fetch failure so callers (LangGraph nodes, the
    Streamlit UI) can catch one exception type instead of every
    possible PyGithub exception."""
    pass


def _get_client(github_token: Optional[str] = None) -> Github:
    token = github_token or os.environ.get("GITHUB_TOKEN")
    if not token:
        raise GitHubFetchError(
            "No GitHub token found. Set the GITHUB_TOKEN env var or pass "
            "github_token= explicitly. See .env.example."
        )
    auth = Auth.Token(token)
    return Github(auth=auth, per_page=100)


def _check_rate_limit(gh: Github, min_remaining: int = 10) -> None:
    """Guard against burning the last few requests mid-loop. If we're
    close to the limit, sleep until reset rather than fail hard.

    Uses gh.rate_limiting / gh.rate_limiting_resettime — PyGithub's
    simple, version-stable properties — rather than get_rate_limit().core,
    whose return shape has changed across PyGithub versions."""
    try:
        remaining, limit = gh.rate_limiting
        reset_epoch = gh.rate_limiting_resettime
    except (GithubException, AttributeError):
        return  # don't let a rate-limit *check* itself break the fetch

    if remaining <= min_remaining:
        wait_seconds = max(0, reset_epoch - time.time()) + 2
        logger.warning(
            "Rate limit low (%s/%s remaining). Sleeping %.0fs until reset.",
            remaining, limit, wait_seconds,
        )
        time.sleep(wait_seconds)


def fetch_pr_diff(
    repo_owner: str,
    repo_name: str,
    pr_number: int,
    github_token: Optional[str] = None,
) -> dict[str, str]:
    """
    Fetch a single PR and return {filename: diff_string}, matching the
    format the rest of the team's code (combine_diffs, the Pull Requests
    UI page) already expects.

    Handles:
        - PRs with 50+ changed files (caps inclusion to the highest-churn
          files, logs how many were skipped)
        - Binary files (included with a clear placeholder instead of
          silently dropped, so agents/UI know a file existed)
        - PRs with zero changes (returns an empty dict — callers already
          check `if not diffs` / `len(diffs) == 0`)
        - Rate limiting (checks remaining quota before fetching, backs
          off if close to the 5000 req/hr ceiling)
        - Missing/invalid PR or repo, bad token (raises GitHubFetchError
          with a clear message instead of a raw PyGithub traceback)

    Raises:
        GitHubFetchError on any failure to fetch.
    """
    gh = _get_client(github_token)
    _check_rate_limit(gh)

    full_repo_name = f"{repo_owner}/{repo_name}"
    try:
        repo = gh.get_repo(full_repo_name)
    except UnknownObjectException:
        raise GitHubFetchError(f"Repo '{full_repo_name}' not found or not accessible.")
    except BadCredentialsException:
        raise GitHubFetchError("Invalid GitHub token — authentication failed.")

    try:
        pr = repo.get_pull(pr_number)
    except UnknownObjectException:
        raise GitHubFetchError(f"PR #{pr_number} not found in {full_repo_name}.")

    try:
        files = list(pr.get_files())
    except RateLimitExceededException:
        _check_rate_limit(gh, min_remaining=0)  # forces the sleep-until-reset path
        files = list(pr.get_files())

    total_files = len(files)
    if total_files == 0:
        return {}

    included_files = files
    if total_files > MAX_FILES_TO_INCLUDE:
        logger.info(
            "PR #%s (%s): %s files changed — including the top %s by change volume.",
            pr_number, full_repo_name, total_files, MAX_FILES_TO_INCLUDE,
        )
        included_files = sorted(
            files, key=lambda f: (f.additions + f.deletions), reverse=True
        )[:MAX_FILES_TO_INCLUDE]

    diffs: dict[str, str] = {}
    binary_count = 0
    truncated_count = 0

    for f in included_files:
        if f.patch is None:
            diffs[f.filename] = BINARY_PLACEHOLDER
            binary_count += 1
            continue

        patch = f.patch
        if len(patch) > MAX_PATCH_CHARS_PER_FILE:
            patch = patch[:MAX_PATCH_CHARS_PER_FILE] + "\n... [patch truncated for length] ..."
            truncated_count += 1

        diffs[f.filename] = patch

    if binary_count:
        logger.info("PR #%s (%s): %s binary/non-diffable file(s) included as placeholders.",
                     pr_number, full_repo_name, binary_count)
    if truncated_count:
        logger.info("PR #%s (%s): %s file(s) had oversized patches truncated.",
                     pr_number, full_repo_name, truncated_count)

    return diffs


def fetch_multiple_prs(
    prs: list[tuple[str, str, int]],
    github_token: Optional[str] = None,
    delay: float = 1.0,
) -> dict[str, dict[str, str]]:
    """
    Batch helper for Member 4 (QA), who needs to run 5-10 real PRs
    through the pipeline.

    Args:
        prs: list of (repo_owner, repo_name, pr_number) tuples.
        delay: seconds to sleep between requests, on top of the
               automatic rate-limit backoff in fetch_pr_diff().

    Returns:
        dict keyed by "owner/repo#pr_number" -> {filename: diff_string},
        or {"_error": "..."} for any PR that failed, so one bad PR
        doesn't kill the whole batch run.
    """
    gh = _get_client(github_token)
    results: dict[str, dict[str, str]] = {}

    for i, (owner, repo_name, pr_number) in enumerate(prs):
        key = f"{owner}/{repo_name}#{pr_number}"
        try:
            _check_rate_limit(gh)
            results[key] = fetch_pr_diff(owner, repo_name, pr_number, github_token)
            logger.info("Fetched %s (%d/%d)", key, i + 1, len(prs))
        except GitHubFetchError as e:
            logger.error("Failed %s: %s", key, e)
            results[key] = {"_error": str(e)}

        if i < len(prs) - 1:
            time.sleep(delay)

    return results


if __name__ == "__main__":
    # Manual smoke test — run `python github_fetcher.py` with GITHUB_TOKEN set.
    diffs = fetch_pr_diff("pallets", "flask", 5665)
    for filename, patch in diffs.items():
        print(f"### FILE: {filename}")
        print(patch[:500])
        print()