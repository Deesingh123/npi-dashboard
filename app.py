import streamlit as st

st.set_page_config(page_title="NPI Dashboard", layout="wide")

# Beautiful CSS
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
        font-size: 1.5rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 80px;
    }
    .card-container {
        display: flex;
        justify-content: center;
        gap: 50px;
        flex-wrap: wrap;
        margin: 0 auto;
        max-width: 1200px;
    }
    .tracker-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 50px 40px;
        border-radius: 20px;
        width: 420px;
        text-align: center;
        box-shadow: 0 15px 40px rgba(102,126,234,0.3);
        transition: all 0.35s ease;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    .tracker-card:hover {
        transform: translateY(-12px);
        box-shadow: 0 30px 60px rgba(102,126,234,0.4);
    }
    .card-icon {
        font-size: 5.5rem;
        margin-bottom: 25px;
    }
    .card-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 12px;
    }
    .card-desc {
        font-size: 1.15rem;
        line-height: 1.6;
        opacity: 0.9;
    }
    .footer-text {
        text-align: center;
        color: #9ca3af;
        font-size: 1.1rem;
        margin-top: 100px;
    }
    @media (max-width: 960px) {
        .card-container { gap: 30px; }
        .tracker-card { width: 90%; }
    }
    @media (max-width: 600px) {
        .main-header { font-size: 3.5rem; }
        .sub-header { font-size: 1.3rem; }
        .card-title { font-size: 1.9rem; }
        .card-desc { font-size: 1rem; }
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🚀 NPI DASHBOARD</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Select a tracker to get started</p>', unsafe_allow_html=True)

# Centered Clickable Cards
col1, col2 = st.columns(2)

with col1:
    if st.button("Process Readiness Tracker", key="readiness_btn", use_container_width=True):
        st.switch_page("pages/1_Process_Readiness.py")
    st.markdown("""
    <div class="tracker-card">
        <div class="card-icon">📋</div>
        <div class="card-title">Process Readiness Tracker</div>
        <div class="card-desc">Track E/F-NRE, queries, quotes, and readiness status</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    if st.button("Milestone Tracker Dashboard", key="milestone_btn", use_container_width=True):
        st.switch_page("pages/2_Milestone_Tracker.py")
    st.markdown("""
    <div class="tracker-card">
        <div class="card-icon">🎯</div>
        <div class="card-title">Milestone Tracker Dashboard</div>
        <div class="card-desc">Monitor WBS & Sub milestones with overdue/pending alerts</div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer-text">
    Live data from Google Sheets • Auto-refresh every 30 seconds • Mobile & desktop friendly
</div>
""", unsafe_allow_html=True)
