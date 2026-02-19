import streamlit as st
from db import init_db

st.set_page_config(page_title="QMS Prototype", layout="wide")
init_db()

st.title("QMS Template – Prototype")
st.caption("Screen #00 – General (For All Users)")

# Simulated user switcher
st.sidebar.header("User Switcher")
username = st.sidebar.selectbox("Logged in as", [
    "mohamed.affify", "qa.compliance", "qa.investigator", "qa.responsible", "compliance.responsible"
])
st.session_state["username"] = username

st.info("Use the left sidebar to switch roles and navigate pages.")

st.subheader("QMS Items")

cols = st.columns(3)
with cols[0]:
    st.markdown("**Non-Quality Event (NQE)**")
    st.page_link("pages/01_NQE_Initiation.py", label="Initiate NQE")
    st.page_link("pages/02_QC_Compliance.py", label="View / QC Review")
    st.page_link("pages/03_Department_Feedback.py", label="Department Feedback")

with cols[1]:
    st.markdown("**Incident (QIN)**")
    st.write("Will appear after classification.")
with cols[2]:
    st.markdown("**Deviation (QDV)**")
    st.write("Will appear after classification.")

st.divider()
st.write("This is a simplified, working prototype designed for review and testing.")
