from github import Github
from config.settings import GITHUB_TOKEN

def fetch_pr_diff(repo_owner, repo_name, pr_number):
    """
    Fetch the diff of a GitHub pull request and return a dictionary of patches.
    """
    print(f"DEBUG: Authenticating for {repo_owner}/{repo_name}...")
    gh = Github(GITHUB_TOKEN)
    
    try:
        repo = gh.get_repo(f"{repo_owner}/{repo_name}")
        print(f"DEBUG: Found repo: {repo.full_name}")
        
        pr = repo.get_pull(pr_number)
        print(f"DEBUG: Successfully accessed PR #{pr_number}")
        
        diffs = {}
        for file in pr.get_files():
            # Debug: See which files are being processed
            print(f"DEBUG: Processing file {file.filename}, patch exists: {bool(file.patch)}")
            if file.patch:
                diffs[file.filename] = file.patch
                
        print(f"DEBUG: Total files with patches found: {len(diffs)}")
        return diffs
        
    except Exception as e:
        print(f"DEBUG ERROR: {e}")
        raise e