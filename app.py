import streamlit as st

st.set_page_config(page_title="NPI Dashboard", layout="wide")

# Custom CSS for larger vertical buttons
st.markdown("""
<style>
    .main-header {
        font-size: 4.8rem;
        font-weight: 800;
        color: #1e40af;
        text-align: center;
        margin: 60px 0 20px 0;
    }
    .sub-header {
        font-size: 1.6rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 100px;
    }
    /* Large vertical buttons */
    div.stButton > button {
        height: 200px !important;           /* Very tall buttons */
        font-size: 2.2rem !important;       /* Large text */
        font-weight: bold !important;
        padding: 30px !important;
        border-radius: 20px !important;
        box-shadow: 0 12px 30px rgba(0,0,0,0.2) !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover {
        transform: translateY(-8px) !important;
        box-shadow: 0 20px 40px rgba(0,0,0,0.3) !important;
    }
    .footer-text {
        text-align: center;
        color: #9ca3af;
        font-size: 1.1rem;
        margin-top: 150px;
    }
    @media (max-width: 960px) {
        div.stButton > button {
            height: 180px !important;
            font-size: 2rem !important;
        }
    }
    @media (max-width: 600px) {
        .main-header { font-size: 3.5rem; }
        .sub-header { font-size: 1.4rem; }
        div.stButton > button {
            height: 160px !important;
            font-size: 1.8rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🚀 NPI DASHBOARD</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Select a tracker to get started</p>', unsafe_allow_html=True)

# Three large vertical buttons (no visual cards)
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📋 UTAH NA ", key="readiness_btn", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Process_Readiness.py")

with col2:
    if st.button("🎯 Milestone Tracker Dashboard", key="milestone_btn", use_container_width=True, type="primary"):
        st.switch_page("pages/2_Milestone_Tracker.py")


with col3:
    if st.button(" 📋 DALLAS NA ", key="risk_btn", use_container_width=True, type="primary"):
        st.switch_page("pages/3_Risk_Issue_Tracker.py")



# Footer
st.markdown("""
<div class="footer-text">
    Live data from Google Sheets • Auto-refresh every 30 seconds • Mobile & desktop friendly
</div>
""", unsafe_allow_html=True)
