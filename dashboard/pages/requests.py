import streamlit as st
import requests
import pandas as pd

st.title("📋 Access Requests")

try:
    response = requests.get("http://127.0.0.1:8000/requests/")

    if response.status_code == 200:
        data = response.json()

        if len(data) > 0:
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No requests found")

    else:
        st.error(response.text)

except Exception as e:
    st.error(f"Error: {e}")
