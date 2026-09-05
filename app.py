import streamlit as st
from datetime import date, datetime
import csv
import os
from io import StringIO

st.set_page_config(page_title="Incident Report", layout="centered")
st.title("Incident Report")

CSV_FILE = "submissions.csv"
FIELDNAMES = ["submitted_at", "incident_date", "severity", "description"]

# Ensure CSV exists with header
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()

# Initialize session state defaults for form fields
if "incident_date" not in st.session_state:
    st.session_state["incident_date"] = date.today()
if "severity" not in st.session_state:
    st.session_state["severity"] = "Medium"
if "description" not in st.session_state:
    st.session_state["description"] = ""

with st.form("incident_form"):
    incident_date = st.date_input("Date of incident", value=st.session_state["incident_date"], key="incident_date")
    description = st.text_area(
        "Description",
        value=st.session_state["description"],
        height=150,
        placeholder="Describe what happened (required)",
        key="description",
    )
    severity = st.selectbox("Severity", ["Low", "Medium", "High"], index=["Low", "Medium", "High"].index(st.session_state["severity"]), key="severity")

    submitted = st.form_submit_button("Submit report")

if submitted:
    # Validation
    if not description or not description.strip():
        st.error("Please provide a description of the incident.")
    else:
        # Append to CSV
        row = {
            "submitted_at": datetime.utcnow().isoformat() + "Z",
            "incident_date": incident_date.isoformat(),
            "severity": severity,
            "description": description.strip(),
        }
        try:
            with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
                writer.writerow(row)
        except Exception as e:
            st.error(f"Failed to save report: {e}")
        else:
            st.success("Incident reported successfully.")
            st.markdown("**Report details:**")
            st.write("- Date of incident:", row["incident_date"])
            st.write("- Severity:", row["severity"])
            st.write("**Description**")
            st.write(row["description"])

            # Reset form fields in session state and rerun to clear the form
            st.session_state["incident_date"] = date.today()
            st.session_state["severity"] = "Medium"
            st.session_state["description"] = ""
            st.experimental_rerun()

# Show past submissions
st.header("Past submissions")
try:
    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
        if reader:
            # Show most recent first
            rows = list(reversed(reader))
            st.write(f"Total reports: {len(rows)}")
            st.dataframe(rows)

            # Provide download button
            with open(CSV_FILE, "r", encoding="utf-8") as f2:
                csv_bytes = f2.read().encode("utf-8")
                st.download_button(label="Download CSV", data=csv_bytes, file_name="incident_reports.csv", mime="text/csv")
        else:
            st.info("No incident reports yet.")
except Exception as e:
    st.error(f"Failed to read submissions: {e}")
