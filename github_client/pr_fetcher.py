from github import Github
from config.settings import GITHUB_TOKEN

def fetch_pr_diff(repo_owner, repo_name, pr_number):
    """
    Fetch the diff of a GitHub pull request.
    Returns a dictionary: {file_path: diff_string}
    """
    gh = Github(GITHUB_TOKEN)
    repo = gh.get_repo(f"{repo_owner}/{repo_name}")
    pr = repo.get_pull(pr_number)

    diffs = {}
    for file in pr.get_files():
        if file.patch:
            diffs[file.filename] = file.patch

    return diffs
