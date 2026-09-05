import streamlit as st
from datetime import date

st.set_page_config(page_title="Incident Report", layout="centered")
st.title("Incident Report")

with st.form("incident_form"):
    incident_date = st.date_input("Date of incident", value=date.today())
    description = st.text_area(
        "Description",
        height=150,
        placeholder="Describe what happened (required)",
    )
    severity = st.selectbox("Severity", ["Low", "Medium", "High"], index=1)

    submitted = st.form_submit_button("Submit report")

if submitted:
    if not description or not description.strip():
        st.error("Please provide a description of the incident.")
    else:
        st.success("Incident reported successfully.")
        st.markdown("**Report details:**")
        st.write("- Date of incident:", incident_date.isoformat())
        st.write("- Severity:", severity)
        st.write("**Description**")
        st.write(description)
