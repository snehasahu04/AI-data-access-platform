import streamlit as st
import requests

st.set_page_config(page_title="Data Access Governance", layout="wide")

st.title("🛡️ Data Access Governance Dashboard")

api_root = st.sidebar.text_input("API Base URL", value="http://localhost:8000")

st.markdown("### Operational Summary")

try:
    requests_response = requests.get(f"{api_root}/requests/")
    approvals_response = requests.get(f"{api_root}/approvals/")
    catalog_response = requests.get(f"{api_root}/catalog/recommend")

    if requests_response.status_code == 200 and approvals_response.status_code == 200:
        requests_data = requests_response.json()
        approvals_data = approvals_response.json()

        total_requests = len(requests_data)
        approved = len([x for x in requests_data if x["status"] == "APPROVED"])
        pending = len([x for x in requests_data if x["status"] == "PENDING_APPROVAL"])
        rejected = len([x for x in requests_data if x["status"] == "REJECTED"])

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Requests", total_requests)
        col2.metric("Approved", approved)
        col3.metric("Pending", pending)
        col4.metric("Rejected", rejected)

        st.markdown("---")
        st.subheader("Recent Approvals")
        st.write(approvals_data[:10])
    else:
        st.error("Unable to fetch governance data from API")

    if catalog_response.status_code == 200:
        st.markdown("---")
        st.subheader("Recommended Datasets")
        st.write(catalog_response.json()[:10])

except Exception as e:
    st.error(f"Error loading governance dashboard: {e}")
