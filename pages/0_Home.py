

import streamlit as st
from theme import ACCENT
from components import html, icon


html("""
    <style>
    section[data-testid="stSidebar"] {display: none;}
    [data-testid="stSidebarCollapsedControl"] {display: none;}
    [data-testid="collapsedControl"] {display: none;}
    </style>
""")


html("""
    <div style="margin-bottom:8px;">
        <div class="cc-landing-logo">◆ CodeCrew</div>
        <div class="cc-landing-tagline">AI-Powered · Multi-Agent · Developer-First</div>
    </div>
""")

st.markdown('<hr style="margin:24px 0 44px 0;">', unsafe_allow_html=True)


hero_l, hero_r = st.columns([1.15, 1], gap="large")

with hero_l:
    html("""
        <h1 style="font-size:3.1rem; line-height:1.15; margin-top:0; margin-bottom:20px; font-weight:800; letter-spacing:-0.02em;">
            Two AI Reviewers.<br>One Smarter Code Review.
        </h1>
    """)
    html("""
        <p style="font-size:1.15rem; color:#6B7280; line-height:1.65; max-width:500px;">
            Paste a diff or a GitHub PR link. Two specialized AI agents review it in parallel
            for bugs, logic errors, security issues, and style — merged into one clean report.
        </p>
    """)
    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    btn_c1, btn_c2 = st.columns([1, 1])
    with btn_c1:
        if st.button("Start Reviewing", type="primary", use_container_width=True):
            st.switch_page("pages/2_Pull_Requests.py")
    with btn_c2:
        
        html('<a href="https://github.com" target="_blank" class="cc-btn-link">View on GitHub</a>')

    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
    f1, f2, f3 = st.columns(3)
    for col, title, desc in [
        (f1, "Catch Critical Issues", "Bugs and security risks before production."),
        (f2, "Save Review Time", "Two agents in parallel, not one long pass."),
        (f3, "Consistent Style", "Same standard applied to every PR."),
    ]:
        with col:
            html(f"""
                <div style="font-weight:700; font-size:0.95rem; margin-bottom:4px;">{title}</div>
                <div class="cc-muted" style="font-size:0.85rem;">{desc}</div>
            """)

with hero_r:
    
    html(f"""
        <div class="cc-card" style="height:100%;">
            <div style="font-weight:700; font-size:1.05rem; margin-bottom:20px;">{icon('summary')}How a review runs</div>
            <div style="display:flex; align-items:center; gap:14px; margin-bottom:20px;">
                <div style="width:36px; height:36px; border-radius:8px; background:{ACCENT}; color:white; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:0.95rem; flex-shrink:0;">1</div>
                <div>
                    <div style="font-weight:700; font-size:0.92rem;">Two agents run in parallel</div>
                    <div class="cc-muted" style="font-size:0.82rem;">Bug & Logic, and Style & Security</div>
                </div>
            </div>
            <div style="display:flex; align-items:center; gap:14px; margin-bottom:20px;">
                <div style="width:36px; height:36px; border-radius:8px; background:{ACCENT}; color:white; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:0.95rem; flex-shrink:0;">2</div>
                <div>
                    <div style="font-weight:700; font-size:0.92rem;">Findings are severity-ranked</div>
                    <div class="cc-muted" style="font-size:0.82rem;">Critical, warning, and info-level issues</div>
                </div>
            </div>
            <div style="display:flex; align-items:center; gap:14px; margin-bottom:26px;">
                <div style="width:36px; height:36px; border-radius:8px; background:{ACCENT}; color:white; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:0.95rem; flex-shrink:0;">3</div>
                <div>
                    <div style="font-weight:700; font-size:0.92rem;">One orchestrated report</div>
                    <div class="cc-muted" style="font-size:0.82rem;">Merged into a single reviewable output</div>
                </div>
            </div>
            <hr style="margin:0 0 20px 0;">
            <div class="cc-issue cc-issue-critical" style="margin-bottom:0;">
                <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                    <span class="cc-chip cc-chip-critical">Critical</span>
                    <span class="cc-issue-meta">example finding</span>
                </div>
                <div class="cc-issue-body" style="font-size:0.9rem;">Password comparison is not constant-time.</div>
                <div class="cc-issue-fix">- if submitted_password == user.password:<br>+ if hmac.compare_digest(...):</div>
            </div>
        </div>
    """)

st.markdown("<div style='height:64px'></div>", unsafe_allow_html=True)
st.divider()
st.markdown("<div style='height:48px'></div>", unsafe_allow_html=True)


html("""
    <div style="text-align:center;">
        <span class="cc-muted" style="font-weight:700; letter-spacing:0.08em; font-size:0.75rem;">HOW IT WORKS</span>
        <h2 style="margin-top:10px; font-size:2.5rem; font-weight:800; letter-spacing:-0.02em;">From PR to report in five steps</h2>
    </div>
""")
st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)

steps = ["GitHub PR", "Diff Parser", "Bug & Logic Agent", "Style & Security Agent", "Orchestrator", "Unified Report"]
cols = st.columns(len(steps))
for i, (col, step) in enumerate(zip(cols, steps)):
    with col:
        html(f"""
            <div style="text-align:center;">
                <div style="width:48px; height:48px; border-radius:12px; background:{ACCENT}; color:white; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:1.15rem; margin:0 auto 14px auto; box-shadow:0 2px 6px rgba(79,70,229,0.25);">{i+1}</div>
                <div style="font-size:0.92rem; font-weight:700;">{step}</div>
            </div>
        """)

st.markdown("<div style='height:56px'></div>", unsafe_allow_html=True)
st.divider()
st.markdown("<div style='height:48px'></div>", unsafe_allow_html=True)


html("""
    <div style="text-align:center;">
        <span class="cc-muted" style="font-weight:700; letter-spacing:0.08em; font-size:0.75rem;">FEATURES</span>
        <h2 style="margin-top:10px; font-size:2.5rem; font-weight:800; letter-spacing:-0.02em;">Built for real code review workflows</h2>
    </div>
""")
st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)

features = [
    ("bug", "Bug Detection", "Logic errors, crash risks, and edge cases caught before merge."),
    ("shield", "Security Analysis", "Common vulnerability patterns flagged with concrete fixes."),
    ("chart", "Parallel Agents", "Bug/logic and style/security run at the same time, not sequentially."),
    ("summary", "Actionable Suggestions", "Every finding ships with a suggested fix, not just a warning."),
    ("code", "GitHub Integration", "Paste a PR URL and CodeCrew pulls the real diff."),
    ("score", "Unified Reports", "One orchestrated report instead of two disconnected outputs."),
]
for row_start in range(0, len(features), 3):
    row = st.columns(3, gap="medium")
    for col, (icon_name, title, desc) in zip(row, features[row_start:row_start + 3]):
        with col:
            html(f"""
                <div class="cc-card" style="min-height:170px; padding:24px;">
                    <div style="width:42px; height:42px; border-radius:9px; background:#EEF2FF; display:flex; align-items:center; justify-content:center; margin-bottom:16px;">{icon(icon_name)}</div>
                    <div style="font-weight:700; font-size:1.05rem; margin-bottom:10px;">{title}</div>
                    <div class="cc-subtle" style="font-size:0.9rem; line-height:1.5;">{desc}</div>
                </div>
            """)
    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

st.markdown("<div style='height:36px'></div>", unsafe_allow_html=True)
html('<div style="text-align:center;" class="cc-muted">◆ CodeCrew — Automating code quality. Ship faster with agentic reviews.</div>')