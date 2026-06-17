import streamlit as st
import pandas as pd
import requests

# Section 1: Header
st.header("Career Application Tracker Dashboard")
st.write("Track job applications, statuses, sources, and progress.")


# Section 2: Backend connection check
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

api_connected = False

try:
    response = requests.get(f"{API_URL}/health", timeout=5)

    if response.status_code == 200:
        api_connected = True
        st.success("API connected")
    else:
        st.error("API is running, but health check failed.")

except requests.exceptions.RequestException:
    st.error("API not running. Please start FastAPI first.")


# Stop dashboard if API is not connected
if not api_connected:
    st.stop()


applications_response = requests.get(f"{API_URL}/applications")
applications = applications_response.json()
df_applications = pd.DataFrame(applications)


companies_response = requests.get(f"{API_URL}/companies")
companies = companies_response.json()
df_companies = pd.DataFrame(companies)


statuses_response = requests.get(f"{API_URL}/statuses")
statuses = statuses_response.json()
df_statuses = pd.DataFrame(statuses)

source_counts_response = requests.get(f"{API_URL}/analytics/source-counts")
source_counts = source_counts_response.json()

if len(source_counts) > 0:
    most_common_source = max(source_counts, key=source_counts.get)
else:
    most_common_source = "N/A"

st.subheader("Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Applications", len(df_applications))
col2.metric("Total Companies", len(df_companies))
col3.metric("Total Statuses", len(df_statuses))
col4.metric("Most Common Source", most_common_source)


# Section 4: Application table and Section 5: Filters
applications_copy = df_applications.copy()

# Filer by company_id
selected_company_id = st.selectbox(
    "Filter by company_id",
    ["All"] + sorted(df_applications["company_id"].unique().tolist())
)

if selected_company_id != "All":
    applications_copy = applications_copy[applications_copy["company_id"] == selected_company_id]


# Filer by source
selected_source = st.selectbox(
    "Filter by source",
    ["All"] + sorted(df_applications["source"].unique().tolist())
)

if selected_source != "All":
    applications_copy = applications_copy[applications_copy["source"] == selected_source]


# Filer by search keyword
selected_search_keyword = st.text_input("Enter job title keyword:")

if selected_search_keyword.strip() != "":
    applications_copy = applications_copy[
        applications_copy["job_title"].str.contains(
            selected_search_keyword, 
            case=False, 
            na=False
        )
    ]

applications_copy.index = range(1, len(applications_copy) + 1)

st.dataframe(applications_copy)


# Section 6: Analytics charts
df_source_counts = pd.DataFrame(list(source_counts.items()), columns=["source", "count"])

company_counts_response = requests.get(f"{API_URL}/analytics/company-counts")
company_counts = company_counts_response.json()
df_company_counts = pd.DataFrame(list(company_counts.items()), columns=["company_id", "count"])


status_counts_response = requests.get(f"{API_URL}/analytics/status-counts")
status_counts = status_counts_response.json()
df_status_counts = pd.DataFrame(list(status_counts.items()), columns=["status", "count"])


df_source_counts["count"] = pd.to_numeric(df_source_counts["count"])
df_company_counts["count"] = pd.to_numeric(df_company_counts["count"])
df_status_counts["count"] = pd.to_numeric(df_status_counts["count"])

st.subheader("Count Summary")

st.write("Count by Company chart")
st.bar_chart(df_company_counts.set_index("company_id")["count"])

st.write("Count by Source chart")
st.bar_chart(df_source_counts.set_index("source")["count"])

st.write("Count by Status chart")
st.bar_chart(df_status_counts.set_index("status")["count"])


# Section 7: Notes / Status Viewer
st.subheader("Application Notes and Status History")

application_id = st.number_input(
    "Enter application ID",
    min_value=1,
    step=1
)

if st.button("View Application Details"):
    try:
        # Check if application exists first
        app_response = requests.get(
            f"{API_URL}/applications/{application_id}",
            timeout=5
        )

        if app_response.status_code == 404:
            st.error("Application not found.")
        else:
            application = app_response.json()

            st.write("Selected Application")
            st.json(application)

            # Get notes
            notes_response = requests.get(
                f"{API_URL}/applications/{application_id}/notes",
                timeout=5
            )

            notes = notes_response.json()
            df_notes = pd.DataFrame(notes)

            st.write("Notes")

            if len(df_notes) > 0:
                df_notes.index = range(1, len(df_notes) + 1)
                st.dataframe(df_notes)
            else:
                st.info("No notes found for this application.")

            # Get status history
            status_response = requests.get(
                f"{API_URL}/applications/{application_id}/status-history",
                timeout=5
            )

            status_history = status_response.json()
            df_status_history = pd.DataFrame(status_history)

            st.write("Status History")

            if len(df_status_history) > 0:
                df_status_history.index = range(1, len(df_status_history)  + 1)
                st.dataframe(df_status_history)
            else:
                st.info("No status history found for this application.")

    except requests.exceptions.RequestException:
        st.error("Could not connect to API.")


# Section 8: Top Skills Chart
skill_count_response = requests.get(f"{API_URL}/analytics/skill-counts")
skill_count = skill_count_response.json()
df_skill_counts = pd.DataFrame(list(skill_count.items()), columns=["skill", "count"])

if len(df_skill_counts) == 0:
    st.info("No skill data available yet.")
else:
    st.write("Count by Skill chart")
    st.bar_chart(df_skill_counts.set_index("skill")["count"])