

import streamlit as st
from components import kpi_card, status_chip, section_header, topbar
from mock_data import SAMPLE_REVIEWS

if "review_history" not in st.session_state:
    st.session_state.review_history = []


all_reviews = st.session_state.review_history + SAMPLE_REVIEWS


tb_l, tb_r = st.columns([3, 1])
with tb_l:
    topbar("CodeCrew / Dashboard", "Welcome back!", "Here's what CodeCrew has reviewed recently.")
with tb_r:
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    if st.button("+ New Review", type="primary", use_container_width=True):
        st.switch_page("pages/2_Pull_Requests.py")


completed = [r for r in all_reviews if r["status"] == "Completed"]
total_critical = sum(r["critical"] or 0 for r in completed)
total_warning = sum(r["warning"] or 0 for r in completed)
avg_score = round(sum(r["score"] or 0 for r in completed) / len(completed)) if completed else 0

k1, k2, k3, k4 = st.columns(4)
with k1:
    kpi_card("Reviews Completed", len(completed), accent="indigo")
with k2:
    kpi_card("Critical Issues Found", total_critical, accent="rose")
with k3:
    kpi_card("Warnings Flagged", total_warning, accent="amber")
with k4:
    kpi_card("Average Score", f"{avg_score}/100", accent="teal")

st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)


section_header("Recent Reviews")

table = st.container(border=True)
with table:
    header = st.columns([2.4, 3, 1.3, 1, 1, 1, 1.2])
    for col, label in zip(header, ["Repository", "Title", "Status", "Critical", "Warning", "Score", ""]):
        col.markdown(f'<span class="cc-muted" style="font-weight:600;">{label}</span>', unsafe_allow_html=True)

    st.markdown('<hr style="margin:8px 0;">', unsafe_allow_html=True)

    for r in all_reviews:
        row = st.columns([2.4, 3, 1.3, 1, 1, 1, 1.2])
        row[0].markdown(f"**{r['repo']}**<br><span class='cc-muted'>#{r['pr_number']} · {r['time_ago']}</span>", unsafe_allow_html=True)
        row[1].markdown(r["title"])
        row[2].markdown(status_chip(r["status"]), unsafe_allow_html=True)
        row[3].markdown(r["critical"] if r["critical"] is not None else "—")
        row[4].markdown(r["warning"] if r["warning"] is not None else "—")
        row[5].markdown(f"{r['score']}" if r["score"] is not None else "—")
        with row[6]:
            row_id = r.get("id", f"{r['repo']}_{r['pr_number']}")
            st.button("View →", key=f"view_{row_id}", use_container_width=True)