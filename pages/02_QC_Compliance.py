import streamlit as st
import pandas as pd
from datetime import datetime
from db import get_conn, init_db, next_seq
from utils import add_working_days

st.set_page_config(page_title="QC Compliance Review")
init_db()

st.title("Quality Compliance Review")
st.caption("Screen #02 – For Quality Compliance Responsible")

username = st.session_state.get("username","guest")
if username != "qa.compliance":
    st.warning('Tip: switch to user "qa.compliance" from the sidebar to act as Compliance.')

with get_conn() as con:
    nqe_df = pd.read_sql_query("SELECT * FROM nqe ORDER BY id DESC", con)

st.subheader("1) Submitted NQEs")
st.dataframe(nqe_df[["id","nqe_no","created_at","created_by","product","batch_no","status"]])

selected_id = st.selectbox("Open NQE ID", nqe_df["id"] if not nqe_df.empty else [])

if selected_id:
    row = nqe_df[nqe_df["id"]==selected_id].iloc[0]
    with st.expander("Summary of Screen #01"):
        st.json(row.to_dict())

    st.subheader("2) Is concerned department feedback needed?")
    need_fb = st.checkbox("Yes, request feedback from departments", value=False)
    depts = st.multiselect("Select Departments", ['Production','Packaging','Engineering','QC','Warehouse','Others']) if need_fb else []

    if need_fb and st.button("Send Feedback Request"):
        due = add_working_days(datetime.now(), 1).strftime("%Y-%m-%d")
        with get_conn() as con:
            cur = con.cursor()
            cur.execute("INSERT INTO qc_review(nqe_id, need_feedback, departments) VALUES (?,?,?)",
                        (int(selected_id), 1, ",".join(depts)))
            con.commit()
        st.success(f"Feedback requested. Due by {due} (1 working day).")
        st.info("Department users can open 'Department Feedback' page to submit.")

    st.subheader("3) Classification Questions")
    q1 = st.radio('Does the event affect a product attribute?', ['No','Yes'], horizontal=True)
    q2 = st.radio('Does the event affect the product`s quality?', ['No','Yes'], horizontal=True)
    q3 = st.radio('Does the event affect a manufacturing operational parameter?', ['No','Yes'], horizontal=True)
    q4 = st.radio('Does the event contradict or omit a requirement/instruction in any approved procedure/specification?', ['No','Yes'], horizontal=True)

    if st.button("Classify & Send to QA Investigation", type="primary"):
        answers = [q1,q2,q3,q4]
        typ = "QDV" if any(a=="Yes" for a in answers) else "QIN"
        no  = next_seq(typ)
        due_days = 30 if typ=="QDV" else 20
        due = add_working_days(datetime.now(), due_days).strftime("%Y-%m-%d")
        with get_conn() as con:
            cur = con.cursor()
            cur.execute("INSERT INTO qc_review(nqe_id, need_feedback, departments, questions, outcome, outcome_no, sent_to_qa, due_date) VALUES (?,?,?,?,?,?,?,?)",
                        (int(selected_id), 1 if need_fb else 0, ",".join(depts), str(answers), typ, no, datetime.now().isoformat(), due))
            # create investigation shell
            cur.execute("INSERT INTO investigation(type, ref_no, nqe_id, title, data, status) VALUES (?,?,?,?,?,?)",
                        (typ, no, int(selected_id), "", "{}", "pending"))
            con.commit()
        st.success(f"Classified as {typ} with number {no}. Sent to QA Investigation. Due {due}.")
