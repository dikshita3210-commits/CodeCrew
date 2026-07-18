
import os
import pytest
from unittest.mock import MagicMock, patch

os.environ.setdefault("GITHUB_TOKEN", "fake-token-for-tests")

from githubfetcher import (
    fetch_pr_diff,
    fetch_multiple_prs,
    GitHubFetchError,
    MAX_FILES_TO_INCLUDE,
    BINARY_PLACEHOLDER,
)


def make_fake_file(filename, patch, additions=5, deletions=2, status="modified"):
    f = MagicMock()
    f.filename = filename
    f.patch = patch
    f.additions = additions
    f.deletions = deletions
    f.status = status
    return f


def make_fake_pr(number=42, title="Fix bug", author="octocat", files=None):
    pr = MagicMock()
    pr.number = number
    pr.title = title
    pr.user.login = author
    pr.get_files.return_value = files or []
    return pr


@pytest.fixture
def mock_github():
    with patch("githubfetcher.Github") as MockGithub:
        instance = MockGithub.return_value
        instance.rate_limiting = (4999, 5000)
        instance.rate_limiting_resettime = 9999999999
        yield instance


class TestBasicFetch:
    def test_normal_pr_with_one_file(self, mock_github):
        pr = make_fake_pr(files=[
            make_fake_file("app.py", "@@ -1,3 +1,4 @@\n+import os\n def f(): pass")
        ])
        mock_github.get_repo.return_value.get_pull.return_value = pr

        result = fetch_pr_diff("octocat", "hello-world", 42)

        assert isinstance(result, dict)
        assert "app.py" in result
        assert "+import os" in result["app.py"]

    def test_multiple_files_included(self, mock_github):
        pr = make_fake_pr(files=[
            make_fake_file("a.py", "@@ diff a @@"),
            make_fake_file("b.py", "@@ diff b @@"),
        ])
        mock_github.get_repo.return_value.get_pull.return_value = pr

        result = fetch_pr_diff("owner", "repo", 1)

        assert result["a.py"] == "@@ diff a @@"
        assert result["b.py"] == "@@ diff b @@"


class TestEdgeCases:
    def test_pr_with_no_changes(self, mock_github):
        pr = make_fake_pr(files=[])
        mock_github.get_repo.return_value.get_pull.return_value = pr

        result = fetch_pr_diff("owner", "repo", 1)

        assert result == {}

    def test_binary_file_included_as_placeholder(self, mock_github):
        pr = make_fake_pr(files=[
            make_fake_file("logo.png", patch=None, status="modified"),
            make_fake_file("main.py", "@@ real diff @@"),
        ])
        mock_github.get_repo.return_value.get_pull.return_value = pr

        result = fetch_pr_diff("owner", "repo", 1)

        assert result["logo.png"] == BINARY_PLACEHOLDER
        assert result["main.py"] == "@@ real diff @@"

    def test_large_pr_over_50_files_is_capped(self, mock_github):
        files = [
            make_fake_file(f"file_{i}.py", f"@@ diff {i} @@", additions=i)
            for i in range(75)
        ]
        pr = make_fake_pr(files=files)
        mock_github.get_repo.return_value.get_pull.return_value = pr

        result = fetch_pr_diff("owner", "repo", 1)

        assert len(result) == MAX_FILES_TO_INCLUDE

    def test_huge_single_patch_gets_truncated(self, mock_github):
        huge_patch = "+line\n" * 5000
        pr = make_fake_pr(files=[make_fake_file("huge.py", huge_patch)])
        mock_github.get_repo.return_value.get_pull.return_value = pr

        result = fetch_pr_diff("owner", "repo", 1)

        assert "truncated for length" in result["huge.py"]

    def test_repo_not_found_raises_clean_error(self, mock_github):
        from github.GithubException import UnknownObjectException
        mock_github.get_repo.side_effect = UnknownObjectException(404, "Not Found", None)

        with pytest.raises(GitHubFetchError, match="not found"):
            fetch_pr_diff("nope", "nope", 1)

    def test_pr_not_found_raises_clean_error(self, mock_github):
        from github.GithubException import UnknownObjectException
        mock_github.get_repo.return_value.get_pull.side_effect = UnknownObjectException(
            404, "Not Found", None
        )

        with pytest.raises(GitHubFetchError, match="PR #999 not found"):
            fetch_pr_diff("owner", "repo", 999)

    def test_missing_token_raises_before_any_call(self, mock_github, monkeypatch):
        monkeypatch.delenv("GITHUB_TOKEN", raising=False)
        with pytest.raises(GitHubFetchError, match="No GitHub token"):
            fetch_pr_diff("owner", "repo", 1, github_token=None)


class TestBatchFetch:
    def test_batch_continues_after_one_failure(self, mock_github):
        from github.GithubException import UnknownObjectException

        good_pr = make_fake_pr(files=[make_fake_file("ok.py", "@@ fine @@")])

        def get_pull_side_effect(number):
            if number == 2:
                raise UnknownObjectException(404, "Not Found", None)
            return good_pr

        mock_github.get_repo.return_value.get_pull.side_effect = get_pull_side_effect

        results = fetch_multiple_prs(
            [("o", "r", 1), ("o", "r", 2), ("o", "r", 3)], delay=0
        )

        assert len(results) == 3
        assert results["o/r#1"]["ok.py"] == "@@ fine @@"
        assert "_error" in results["o/r#2"]
        assert results["o/r#3"]["ok.py"] == "@@ fine @@"


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-v"]))