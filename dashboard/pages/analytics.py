import streamlit as st
import requests

st.title("📊 Analytics Dashboard")

try:
    requests_response = requests.get(
        "http://127.0.0.1:8000/requests/"
    )

    if requests_response.status_code == 200:

        data = requests_response.json()

        total_requests = len(data)

        approved = len(
            [x for x in data if x["status"] == "APPROVED"]
        )

        pending = len(
            [x for x in data if x["status"] == "PENDING_APPROVAL"]
        )

        rejected = len(
            [x for x in data if x["status"] == "REJECTED"]
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Requests",
            total_requests
        )

        col2.metric(
            "Approved",
            approved
        )

        col3.metric(
            "Pending",
            pending
        )

        col4.metric(
            "Rejected",
            rejected
        )

    else:
        st.error("Unable to fetch request data")

except Exception as e:
    st.error(f"Error: {e}")