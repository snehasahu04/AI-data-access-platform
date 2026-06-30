import streamlit as st

st.set_page_config(page_title="AI Data Access Platform", page_icon="🔐", layout="wide")

st.title("🔐 AI Data Access Provisioning Platform")

st.markdown("---")

st.subheader("Welcome")

st.write("""
This dashboard helps manage data access requests,
approvals, and analytics.

Use the navigation menu on the left side to access:

✅ Requests

✅ Approvals

✅ Analytics
""")

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("📋 View Access Requests")

with col2:
    st.success("✅ Manage Approvals")

with col3:
    st.warning("📊 View Analytics")
