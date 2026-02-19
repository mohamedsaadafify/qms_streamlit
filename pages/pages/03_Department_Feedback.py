import streamlit as st
import pandas as pd
from db import get_conn, init_db

st.set_page_config(page_title="Department Feedback")
init_db()

st.title("Department Feedback")
st.caption("Screen #03 – For Concerned Department Users")

with get_conn() as con:
    pending = pd.read_sql_query("""
        SELECT nqe.id as nqe_id, nqe.nqe_no, nqe.product, nqe.batch_no
        FROM nqe 
        JOIN qc_review qr ON qr.nqe_id = nqe.id
        WHERE qr.need_feedback = 1
        ORDER BY nqe.id DESC
    """, con)

st.dataframe(pending)

if not pending.empty:
    sel = st.selectbox("Select NQE to give feedback", pending["nqe_id"])
    fb = st.text_area("Feedback")
    if st.button("Submit Feedback"):
        with get_conn() as con:
            cur = con.cursor()
            cur.execute("INSERT INTO dept_feedback(nqe_id, department, feedback, created_at) VALUES (?,?,?,datetime('now'))",
                        (int(sel), "Auto-From-User", fb))
            con.commit()
        st.success("Feedback submitted.")
else:
    st.info("No pending feedback requests.")
