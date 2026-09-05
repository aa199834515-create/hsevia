import os
import sqlite3
from datetime import datetime, date
import uuid
import pandas as pd
import streamlit as st
from db import init_db, insert_report, query_reports

# Constants
DB_PATH = "hsevia.db"
UPLOAD_DIR = "uploads"
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5 MB

# Ensure upload dir exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.set_page_config(page_title="HSEvia - HSE Portal", layout="wide")

# Initialize DB
init_db(DB_PATH)

# Sidebar navigation
st.sidebar.title("HSEvia")
page = st.sidebar.radio("Go to", ["Home", "Report Incident", "Reports (Admin)", "Resources"])

# Helper to show report details
def show_report_details(r):
    st.subheader(f"Report #{r['id']} — {r['incident_date']}")
    st.write("Submitted at:", r['submitted_at'])
    st.write("Reporter:", r.get('reporter') or "-")
    st.write("Department:", r.get('department') or "-")
    st.write("Location:", r.get('location') or "-")
    st.write("Severity:", r.get('severity'))
    st.write("Description:")
    st.write(r.get('description'))
    if r.get('attachment_path'):
        st.write("Attachment:")
        try:
            st.download_button("Download attachment", data=open(r['attachment_path'], "rb"), file_name=os.path.basename(r['attachment_path']))
        except Exception:
            st.write("(Could not open attachment)")

# Pages
if page == "Home":
    st.title("Welcome to HSEvia")
    st.markdown(
        """
        HSEvia is a simple Health, Safety & Environment portal for reporting incidents and viewing past reports.

        Use the "Report Incident" page to submit a new incident. Administrators can review reports on the "Reports (Admin)" page.
        """
    )
    st.markdown("---")
    st.subheader("Contact")
    st.write("Email: hse-support@example.com")
    st.write("Phone: +1 (555) 123-4567")

elif page == "Report Incident":
    st.title("Report an Incident")

    with st.form("incident_form"):
        incident_date = st.date_input("Date of incident", value=date.today())
        reporter = st.text_input("Reporter name (optional)")
        department = st.text_input("Department (optional)")
        location = st.text_input("Location (optional)")
        severity = st.selectbox("Severity", ["Low", "Medium", "High"], index=1)
        description = st.text_area("Description", height=200, placeholder="Describe what happened (required)")
        attachment = st.file_uploader("Attachment (optional, max 5MB)", type=["png","jpg","jpeg","pdf"], accept_multiple_files=False)

        submitted = st.form_submit_button("Submit report")

    if submitted:
        if not description or not description.strip():
            st.error("Please provide a description of the incident.")
        else:
            attachment_path = None
            if attachment is not None:
                # Check size
                attachment.seek(0, os.SEEK_END)
                size = attachment.tell()
                attachment.seek(0)
                if size > MAX_UPLOAD_SIZE:
                    st.error("Attachment is too large (max 5 MB). Please remove or reduce the file size.")
                    st.stop()

                # Save file with UUID name to avoid collisions
                ext = os.path.splitext(attachment.name)[1]
                fname = f"{uuid.uuid4().hex}{ext}"
                attachment_path = os.path.join(UPLOAD_DIR, fname)
                with open(attachment_path, "wb") as f:
                    f.write(attachment.getbuffer())

            row = {
                "incident_date": incident_date.isoformat(),
                "reporter": reporter.strip() if reporter else None,
                "department": department.strip() if department else None,
                "location": location.strip() if location else None,
                "severity": severity,
                "description": description.strip(),
                "attachment_path": attachment_path,
                "submitted_at": datetime.utcnow().isoformat() + "Z",
            }

            try:
                insert_report(DB_PATH, row)
            except Exception as e:
                st.error(f"Failed to save report: {e}")
            else:
                st.success("Incident reported successfully.")
                st.write("Report details:")
                st.write(f"- Date of incident: {row['incident_date']}")
                st.write(f"- Severity: {row['severity']}")
                st.write(f"- Reporter: {row.get('reporter') or '-'}")
                st.write("- Description:")
                st.write(row['description'])

elif page == "Reports (Admin)":
    st.title("Reports — Admin")
    admin_password = os.environ.get("STREAMLIT_ADMIN_PASSWORD")

    if not admin_password:
        st.warning("No admin password is configured. Set STREAMLIT_ADMIN_PASSWORD in the environment to enable admin access.")
        st.stop()

    pw = st.text_input("Admin password", type="password")
    if pw != admin_password:
        st.error("Invalid admin password")
        st.stop()

    # Show filters and reports
    st.subheader("Filters")
    df = query_reports(DB_PATH)
    if df.empty:
        st.info("No reports yet.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            sev_filter = st.multiselect("Severity", options=["Low","Medium","High"], default=["Low","Medium","High"])
        with col2:
            date_from = st.date_input("From", value=None)
            date_to = st.date_input("To", value=None)

        filtered = df[df['severity'].isin(sev_filter)]
        if date_from:
            filtered = filtered[filtered['incident_date'] >= pd.to_datetime(date_from).date().isoformat()]
        if date_to:
            filtered = filtered[filtered['incident_date'] <= pd.to_datetime(date_to).date().isoformat()]

        st.write(f"Showing {len(filtered)} reports")
        st.dataframe(filtered)

        # Download CSV
        csv = filtered.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", data=csv, file_name="hse_reports.csv", mime="text/csv")

        # Expand per-report details
        for _, r in filtered.sort_values('id', ascending=False).iterrows():
            with st.expander(f"Report #{r['id']} — {r['incident_date']} — {r['severity']}"):
                show_report_details(r)

elif page == "Resources":
    st.title("Resources")
    st.markdown("- HSE Policy (placeholder)")
    st.markdown("- Emergency Contacts (placeholder)")
    st.markdown("You can add resource links or files by editing the repository's resources list.")
