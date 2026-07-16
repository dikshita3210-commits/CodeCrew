

import streamlit as st
from theme import inject_css

st.set_page_config(
    page_title="CodeCrew — Multi-Agent Code Reviewer",
    page_icon="◆",
    layout="wide",
)
inject_css()

home = st.Page("pages/0_Home.py", title="Home", icon=":material/home:", default=True)
dashboard = st.Page("pages/1_Dashboard.py", title="Dashboard", icon=":material/dashboard:")
pull_requests = st.Page("pages/2_Pull_Requests.py", title="Pull Requests", icon=":material/call_merge:")
live_review = st.Page("pages/3_Live_Review.py", title="Live Review", icon=":material/bolt:")
report = st.Page("pages/4_Report.py", title="Report", icon=":material/description:")

pg = st.navigation([home, dashboard, pull_requests, live_review, report])

with st.sidebar:
    st.markdown(
        """<div class="cc-sidebar-footer">
        <hr style="border-color:#1F2937; margin:0 0 12px 0;">
        <span style="font-size:1.05rem; font-weight:800; color:#FFFFFF;">◆ CodeCrew</span><br>
        <span style="font-size:0.75rem; color:#6B7280;">Multi-Agent Code Reviewer</span>
        </div>""",
        unsafe_allow_html=True,
    )

pg.run()