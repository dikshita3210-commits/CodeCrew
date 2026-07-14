import streamlit as st
from github_client.pr_fetcher import fetch_pr_diff
from utils.diff_parser import combine_diffs, truncate_diff
from orchestrator.graph import build_graph
from config.settings import GITHUB_TOKEN

st.set_page_config(page_title="CodeCrew", page_icon="🐛", layout="wide")
st.title("CodeCrew — Multi-Agent Code Review")
st.markdown("Enter a GitHub repo and PR number to run the AI review pipeline.")

col1, col2 = st.columns(2)
with col1:
    repo_input = st.text_input("Repository", placeholder="e.g., pallets/flask")
with col2:
    pr_input = st.text_input("PR Number", placeholder="e.g., 5001", type="default")

if st.button("Run Review", type="primary"):
    if not repo_input or not pr_input:
        st.error("Please enter both repository and PR number.")
    else:
        repo_input = repo_input.strip()
        pr_input = pr_input.strip()

        try:
            repo_owner, repo_name = repo_input.split("/")
            repo_owner = repo_owner.strip()
            repo_name = repo_name.strip()
            pr_number = int(pr_input)
        except ValueError:
            st.error("Invalid format. Repository must be in 'owner/repo' format and PR number must be an integer.")
            st.stop()

        try:
            with st.spinner("Fetching PR diff from GitHub..."):
                diffs = fetch_pr_diff(repo_owner, repo_name, pr_number)

                if len(diffs) == 0:
                    st.warning(f"No file diffs found for PR #{pr_number}. This PR might have no code changes.")
                    st.stop()

                code_diff = combine_diffs(diffs)
                code_diff = truncate_diff(code_diff)
                st.success(f"Fetched {len(diffs)} changed files")

            with st.spinner("Running Bug Reviewer Agent..."):
                graph = build_graph()
                result = graph.invoke({
                    "code_diff": code_diff,
                    "bug_feedback": None,
                    "style_feedback": None,
                    "final_report": None,
                    "iterations": 0
                })

            st.subheader("Final Review Report")
            st.markdown(result["final_report"])

        except Exception as e:
            error_msg = str(e)
            st.error(f"Error: {error_msg}")

            if "404" in error_msg:
                st.warning("This could mean:")
                st.markdown("1. The repo or PR number doesn't exist")
                st.markdown("2. The repo is private and your token doesn't have `repo` scope")
                st.markdown("3. The repo name is wrong — use the format `owner/repo` exactly as it appears on GitHub")
                st.info("Try: `pallets/flask` with PR `5001`, or `psf/requests` with PR `6000`")
