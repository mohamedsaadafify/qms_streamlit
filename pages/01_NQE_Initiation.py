import streamlit as st
from datetime import datetime
from db import get_conn, init_db, next_seq

st.set_page_config(page_title="Initiate NQE")
init_db()

st.title("Initiate NQE")
st.caption("Screen #01 – For All Users")

username = st.session_state.get("username", "guest")

# 1) Auto-assigned
st.subheader("1) Auto-assigned")
c1, c2, c3 = st.columns(3)
with c1:
    st.text_input("NQE# (auto)", value="Will be assigned on submit", disabled=True)
with c2:
    # use a plain hyphen in the time format to avoid smart characters
    st.text_input("Date/Time stamp", value=datetime.now().strftime("%d/%m/%Y - %H:%M"), disabled=True)
with c3:
    st.text_input("Created by", value=username, disabled=True)

# 2) General Information
st.subheader("2) General Information")
product = st.text_input("Product Name/Strength or Process Description")
batch_no = st.text_input("Batch No.")
deviated_code = st.text_input("Deviated item code")
occurrence = st.text_input("Date of occurrence (date/time, duration, shift)")
discovery = st.text_input("Date of discovery")
initiated_dept = st.text_input("Initiated Department")

# 3) Event Description
st.subheader("3) Event Description")
what = st.text_area("What happened? (objective, expected requirement/spec vs. observed)")
why_dev = st.text_area("Why this considered as deviation?")
who = st.text_input("Who discovered this?")
where = st.text_input("Where did it occur? (site, building, room, line, M/C ID)")
how = st.text_input("How was it discovered? (routine check, IPC, alarm, complaint)")

# 4) Immediate Actions
st.subheader("4) Immediate Actions")
containment = st.text_area("Containment (Actions taken to stop the event from continuing)")
corrections = st.text_area("Corrections (The activity corrected the event)")
mitigate = st.text_area("Mitigating Actions (Actions taken to allow for continuity of process)")

if st.button("Submit NQE", type="primary"):
    with get_conn() as con:
        cur = con.cursor()
        cur.execute(
            """
            INSERT INTO nqe(
                nqe_no, created_at, created_by, product, batch_no, deviated_code, occurrence,
                discovery_date, initiated_department, what_happened, why_deviation, who_discovered,
                where_occur, how_discovered, containment, corrections, mitigating_actions, status
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                next_seq("NQE"),
                datetime.now().isoformat(),
                username,
                product,
                batch_no,
                deviated_code,
                occurrence,
                discovery,
                initiated_dept,
                what,
                why_dev,
                who,
                where,
                how,
                containment,
                corrections,
                mitigate,
                "submitted",
            ),
        )
        con.commit()
    st.success("NQE submitted. QC Compliance can now review it from the QC Review page.")