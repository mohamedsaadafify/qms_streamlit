import sqlite3
from utils import today_yy

DB_PATH = 'qms.sqlite'

SCHEMA = """
CREATE TABLE IF NOT EXISTS counters (
    type TEXT NOT NULL,
    yy   TEXT NOT NULL,
    seq  INTEGER NOT NULL,
    PRIMARY KEY(type, yy)
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username   TEXT,
    department TEXT,
    role       TEXT
);

CREATE TABLE IF NOT EXISTS nqe (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nqe_no TEXT, created_at TEXT, created_by TEXT,
    product TEXT, batch_no TEXT, deviated_code TEXT,
    occurrence TEXT, discovery_date TEXT, initiated_department TEXT,
    what_happened TEXT, why_deviation TEXT, who_discovered TEXT,
    where_occur TEXT, how_discovered TEXT,
    containment TEXT, corrections TEXT, mitigating_actions TEXT,
    status TEXT DEFAULT 'submitted'
);

CREATE TABLE IF NOT EXISTS qc_review (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nqe_id INTEGER, need_feedback INTEGER DEFAULT 0, departments TEXT,
    questions JSON, outcome TEXT, outcome_no TEXT, sent_to_qa TEXT, due_date TEXT,
    FOREIGN KEY(nqe_id) REFERENCES nqe(id)
);

CREATE TABLE IF NOT EXISTS dept_feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nqe_id INTEGER, department TEXT, feedback TEXT, created_at TEXT,
    FOREIGN KEY(nqe_id) REFERENCES nqe(id)
);

CREATE TABLE IF NOT EXISTS investigation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT, ref_no TEXT, nqe_id INTEGER, title TEXT,
    data JSON, status TEXT DEFAULT 'draft',
    FOREIGN KEY(nqe_id) REFERENCES nqe(id)
);

CREATE TABLE IF NOT EXISTS signatures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    investigation_id INTEGER, stage TEXT, username TEXT, comment TEXT, signed_at TEXT,
    FOREIGN KEY(investigation_id) REFERENCES investigation(id)
);
"""

def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    with get_conn() as con:
        con.executescript(SCHEMA)
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM users")
        if cur.fetchone()[0] == 0:
            users = [
                ('mohamed.affify','Production','dept_user'),
                ('qa.compliance','QA','qc_responsible'),
                ('qa.investigator','QA','qa_investigator'),
                ('qa.responsible','QA','qa_responsible'),
                ('compliance.responsible','QA','compliance_responsible')
            ]
            cur.executemany("INSERT INTO users(username,department,role) VALUES (?,?,?)", users)
            con.commit()

def next_seq(prefix):
    yy = today_yy()
    with get_conn() as con:
        cur = con.cursor()
        cur.execute("SELECT seq FROM counters WHERE type=? AND yy=?", (prefix, yy))
        row = cur.fetchone()
        if row:
            seq = row[0] + 1
            cur.execute("UPDATE counters SET seq=? WHERE type=? AND yy=?", (seq, prefix, yy))
        else:
            seq = 1
            cur.execute("INSERT INTO counters(type, yy, seq) VALUES (?,?,?)", (prefix, yy, seq))
        con.commit()
    return f"{prefix}-{yy}-{seq:03d}"
