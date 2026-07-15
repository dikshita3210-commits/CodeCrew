
import re
import streamlit as st
from components import topbar, section_header, stat_pill, html
from theme import ACCENT

USE_MOCK = True

if not USE_MOCK:
    from github_client.pr_fetcher import fetch_pr_diff
    from utils.diff_parser import combine_diffs, truncate_diff


def parse_pr_url(url: str):
    match = re.search(r"github\.com/([^/]+)/([^/]+)/pull/(\d+)", url)
    if not match:
        return None
    owner, repo, number = match.groups()
    return owner, repo, int(number)


topbar("CodeCrew / Pull Requests", "Start a Review", "Paste a diff directly, or point CodeCrew at a GitHub PR.")

if "review_history" not in st.session_state:
    st.session_state.review_history = []
if "pr_input_mode" not in st.session_state:
    st.session_state.pr_input_mode = "diff"

left, right = st.columns([1.5, 1], gap="large")

code_diff = ""
pr_meta = None

with left:
    
    card = st.container(border=True)
    with card:
        mode_label = "Diff mode" if st.session_state.pr_input_mode == "diff" else "PR URL mode"
        mode_color = "cc-chip-accent" if st.session_state.pr_input_mode == "diff" else "cc-chip-info"
        html(f"""
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div><span class="cc-step-badge">1</span><span style="font-weight:700; font-size:0.95rem;">Choose an input method</span></div>
                <span class="cc-chip {mode_color}">{mode_label}</span>
            </div>
        """)
        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

        
        seg1, seg2 = st.columns(2)
        with seg1:
            if st.button(
                "Paste a Diff",
                use_container_width=True,
                type="primary" if st.session_state.pr_input_mode == "diff" else "secondary",
            ):
                st.session_state.pr_input_mode = "diff"
                st.rerun()
        with seg2:
            if st.button(
                "GitHub PR URL",
                use_container_width=True,
                type="primary" if st.session_state.pr_input_mode == "url" else "secondary",
            ):
                st.session_state.pr_input_mode = "url"
                st.rerun()

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        if st.session_state.pr_input_mode == "diff":
            code_diff = st.text_area(
                "Diff",
                height=260,
                placeholder="def calculate_total(price, quantity):\n-   return price * quantity\n+   if quantity < 0:\n+       raise ValueError(...)\n+   return price * quantity",
                label_visibility="collapsed",
            )
        else:
            pr_url = st.text_input(
                "GitHub PR URL",
                placeholder="https://github.com/owner/repo/pull/123",
                label_visibility="collapsed",
            )
            if pr_url:
                parsed = parse_pr_url(pr_url)
                if not parsed:
                    st.warning("That doesn't look like a valid GitHub PR URL.")
                elif USE_MOCK:
                    st.info("Mock mode — using sample diff instead of a real GitHub fetch.")
                    owner, repo, number = parsed
                    pr_meta = {"repo": f"{owner}/{repo}", "pr_number": number}
                    code_diff = (
                        "def calculate_total(price, quantity):\n"
                        "-   return price * quantity\n"
                        "+   if quantity < 0:\n"
                        "+       raise ValueError('quantity cannot be negative')\n"
                        "+   return price * quantity"
                    )
                else:
                    owner, repo, number = parsed
                    try:
                        with st.spinner("Fetching PR diff from GitHub..."):
                            diffs = fetch_pr_diff(owner, repo, number)
                            if not diffs:
                                st.warning(f"No file diffs found for PR #{number}.")
                            else:
                                code_diff = truncate_diff(combine_diffs(diffs))
                                pr_meta = {"repo": f"{owner}/{repo}", "pr_number": number, "files_changed": len(diffs)}
                                st.success(f"Fetched {len(diffs)} changed file(s)")
                    except Exception as e:
                        st.error(f"Error fetching PR: {e}")

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    start_disabled = not code_diff.strip()
    if st.button("Start Review →", type="primary", disabled=start_disabled):
        st.session_state.pending_diff = code_diff
        st.session_state.pending_pr_meta = pr_meta
        st.switch_page("pages/3_Live_Review.py")
    if start_disabled:
        st.caption("Paste a diff or a valid PR URL to continue.")

with right:
    section_header("This Session")
    history = st.session_state.review_history
    s1, s2 = st.columns(2)
    with s1:
        stat_pill("Reviews Run", len(history), color=ACCENT)
    with s2:
        avg = round(sum(h["score"] for h in history) / len(history)) if history else "—"
        stat_pill("Avg Score", avg, color="#0D9488")

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    section_header("Your Recent Reviews", "Jump back into something you've already run.")
    if not history:
        html('<div class="cc-card-tight cc-muted">No reviews run yet this session — start one on the left.</div>')
    else:
        for r in history[:4]:
            html(f"""
                <div class="cc-card-tight" style="margin-bottom:10px;">
                    <div style="font-weight:600; font-size:0.85rem;">{r['repo']} <span class="cc-muted">#{r['pr_number']}</span></div>
                    <div class="cc-muted" style="margin-top:4px;">Score {r['score']}/100 · {r['time_ago']}</div>
                </div>
            """)