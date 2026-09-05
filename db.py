import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    submitted_at TEXT NOT NULL,
    incident_date TEXT NOT NULL,
    reporter TEXT,
    department TEXT,
    location TEXT,
    severity TEXT NOT NULL,
    description TEXT NOT NULL,
    attachment_path TEXT
);
"""


def init_db(db_path: str = "hsevia.db"):
    conn = sqlite3.connect(db_path)
    try:
        conn.executescript(SCHEMA)
        conn.commit()
    finally:
        conn.close()


def insert_report(db_path: str, row: dict):
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO reports (submitted_at, incident_date, reporter, department, location, severity, description, attachment_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                row['submitted_at'],
                row['incident_date'],
                row.get('reporter'),
                row.get('department'),
                row.get('location'),
                row['severity'],
                row['description'],
                row.get('attachment_path'),
            ),
        )
        conn.commit()
    finally:
        conn.close()


def query_reports(db_path: str) -> pd.DataFrame:
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql_query("SELECT * FROM reports", conn, parse_dates=False)
        # Normalize incident_date to ISO date strings
        if not df.empty:
            df['incident_date'] = pd.to_datetime(df['incident_date']).dt.date.astype(str)
        return df
    finally:
        conn.close()
