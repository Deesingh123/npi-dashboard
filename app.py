import streamlit as st

st.set_page_config(page_title="NPI Dashboard", layout="wide")

st.markdown("""
<style>
    .main-header {
        font-size: 4.5rem;
        color: #1e40af;
        text-align: center;
        margin-bottom: 10px;
        font-weight: 800;
    }
    .sub-header {
        text-align: center;
        color: #64748b;
        font-size: 1.3rem;
        margin-bottom: 50px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🚀 NPI DASHBOARD</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Select a tracker from the sidebar on the left</p>', unsafe_allow_html=True)

st.info("👈 Use the navigation menu on the left to switch between Process Readiness and Milestone Tracker")
st.caption("Both trackers auto-refresh every 30 seconds with live data from Google Sheets")