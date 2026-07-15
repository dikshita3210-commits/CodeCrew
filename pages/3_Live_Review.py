

import time
import uuid
import streamlit as st
from components import topbar, render_stepper, count_severities, compute_score

USE_MOCK = True

if not USE_MOCK:
    from orchestrator.graph import build_graph

if "pending_diff" not in st.session_state or not st.session_state.pending_diff:
    st.warning("No diff to review yet.")
    if st.button("← Go pick a PR"):
        st.switch_page("pages/2_Pull_Requests.py")
    st.stop()

code_diff = st.session_state.pending_diff
pr_meta = st.session_state.get("pending_pr_meta") or {}

topbar(
    "CodeCrew / Live Review",
    "Reviewing " + (pr_meta.get("repo", "your diff")),
    f"PR #{pr_meta['pr_number']}" if pr_meta.get("pr_number") else "Pasted diff",
)



def run_pipeline_mock(diff: str):
    bug_feedback = (
        "- Severity: CRITICAL\n"
        "  File/Line: app.py, line 12\n"
        "  Issue: No validation for negative quantity before calculation.\n"
        "  Fix: Raise ValueError if quantity < 0.\n\n"
        "- Severity: INFO\n"
        "  File/Line: app.py, general\n"
        "  Issue: Function is missing a docstring.\n"
        "  Fix: Add a short docstring describing expected inputs.\n"
    )
    style_feedback = (
        "- Severity: WARNING\n"
        "  File/Line: app.py, line 4\n"
        "  Issue: Variable name 'qty' inconsistent with 'quantity' used elsewhere.\n"
        "  Fix: Rename to 'quantity' for consistency.\n\n"
        "- Severity: INFO\n"
        "  File/Line: app.py, general\n"
        "  Issue: No hardcoded secrets or SQL injection risk detected.\n"
        "  Fix: No action needed.\n"
    )
    final_report = (
        "**SUMMARY**: Small change adding input validation; mostly solid, one missing check.\n\n"
        "**CRITICAL ISSUES**: Missing validation for negative quantity.\n\n"
        "**WARNINGS**: Inconsistent variable naming.\n\n"
        "**SUGGESTIONS**: Add docstring.\n\n"
        "**OVERALL VERDICT**: REQUEST CHANGES"
    )
    return bug_feedback, style_feedback, final_report


def run_pipeline_real(diff: str):
    graph = build_graph()
    result = graph.invoke({
        "code_diff": diff,
        "bug_feedback": None,
        "style_feedback": None,
        "final_report": None,
        "iterations": 0,
    })
    return result["bug_feedback"], result["style_feedback"], result["final_report"]


stages = [
    "Parsing diff",
    "Bug & Logic Agent running",
    "Style & Security Agent running",
    "Orchestrator merging results",
]

if "live_review_done" not in st.session_state:
    st.session_state.live_review_done = False

left, right = st.columns([1.3, 1], gap="large")


with right:
    meta_card = st.container(border=True)
    with meta_card:
        st.markdown('<div style="font-weight:700; font-size:0.9rem; margin-bottom:10px;">Reviewing</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="cc-muted" style="margin-bottom:14px;">
                {pr_meta.get('repo', 'Pasted diff')}
                {' · PR #' + str(pr_meta['pr_number']) if pr_meta.get('pr_number') else ''}
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.code(code_diff, language="diff")

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    agents_card = st.container(border=True)
    with agents_card:
        st.markdown('<div style="font-weight:700; font-size:0.9rem; margin-bottom:12px;">Agents on this review</div>', unsafe_allow_html=True)
        a1, a2 = st.columns(2)
        with a1:
            st.markdown(
                """
                <div class="cc-card-tight cc-accent-indigo">
                    <div style="font-weight:600; font-size:0.82rem;">Agent 1</div>
                    <div class="cc-muted">Bug & Logic</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with a2:
            st.markdown(
                """
                <div class="cc-card-tight cc-accent-teal">
                    <div style="font-weight:600; font-size:0.82rem;">Agent 2</div>
                    <div class="cc-muted">Style & Security</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


with left:
    if not st.session_state.live_review_done:
        card = st.container(border=True)
        with card:
            st.markdown('<div style="font-weight:700; font-size:0.9rem; margin-bottom:6px;">Pipeline status</div>', unsafe_allow_html=True)
            stepper_placeholder = st.empty()
            bar = st.progress(0)

            for i, stage in enumerate(stages):
                stepper_placeholder.markdown(render_stepper(stages, i), unsafe_allow_html=True)
                bar.progress(int((i + 1) / (len(stages) + 1) * 100))
                time.sleep(0.7)

            try:
                if USE_MOCK:
                    bug_feedback, style_feedback, final_report = run_pipeline_mock(code_diff)
                else:
                    bug_feedback, style_feedback, final_report = run_pipeline_real(code_diff)
            except Exception as e:
                st.error(f"Pipeline error: {e}")
                if not USE_MOCK:
                    st.info("If this is a connection error, make sure Ollama is running: `ollama serve`")
                st.stop()

            bar.progress(100)
            stepper_placeholder.markdown(render_stepper(stages, len(stages)), unsafe_allow_html=True)

        st.session_state.result = (bug_feedback, style_feedback, final_report)
        st.session_state.diff_shown = code_diff
        st.session_state.live_review_done = True

        bc = count_severities(bug_feedback)
        sc = count_severities(style_feedback)
        st.session_state.setdefault("review_history", [])
        st.session_state.review_history.insert(0, {
            "id": str(uuid.uuid4()),
            "repo": pr_meta.get("repo", "pasted-diff"),
            "pr_number": pr_meta.get("pr_number", "—"),
            "title": "Manual review" if not pr_meta else "PR review",
            "author": "kanikakhati",
            "status": "Completed",
            "critical": bc["critical"] + sc["critical"],
            "warning": bc["warning"] + sc["warning"],
            "info": bc["info"] + sc["info"],
            "score": compute_score(bc, sc),
            "files_changed": pr_meta.get("files_changed", 1),
            "time_ago": "just now",
        })
        st.rerun()

    else:
        card = st.container(border=True)
        with card:
            st.markdown('<div style="font-weight:700; font-size:0.9rem; margin-bottom:6px;">Pipeline status</div>', unsafe_allow_html=True)
            st.markdown(render_stepper(stages, len(stages)), unsafe_allow_html=True)

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

       
        bug_feedback, style_feedback, final_report = st.session_state.result
        bc = count_severities(bug_feedback)
        sc = count_severities(style_feedback)
        total_critical = bc["critical"] + sc["critical"]
        total_warning = bc["warning"] + sc["warning"]
        total_info = bc["info"] + sc["info"]

        glance = st.container(border=True)
        with glance:
            st.markdown('<div style="font-weight:700; font-size:0.9rem; margin-bottom:10px;">Quick glance</div>', unsafe_allow_html=True)
            g1, g2, g3 = st.columns(3)
            g1.markdown(f'<div style="text-align:center;"><div style="font-size:1.3rem; font-weight:800; color:#DC2626;">{total_critical}</div><div class="cc-muted">Critical</div></div>', unsafe_allow_html=True)
            g2.markdown(f'<div style="text-align:center;"><div style="font-size:1.3rem; font-weight:800; color:#D97706;">{total_warning}</div><div class="cc-muted">Warning</div></div>', unsafe_allow_html=True)
            g3.markdown(f'<div style="text-align:center;"><div style="font-size:1.3rem; font-weight:800; color:#059669;">{total_info}</div><div class="cc-muted">Info</div></div>', unsafe_allow_html=True)

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            if st.button("View Full Report →", type="primary", use_container_width=True):
                st.session_state.live_review_done = False
                st.switch_page("pages/4_Report.py")
        with c2:
            if st.button("Run another review", type="secondary", use_container_width=True):
                st.session_state.live_review_done = False
                st.session_state.pending_diff = None
                st.switch_page("pages/2_Pull_Requests.py")