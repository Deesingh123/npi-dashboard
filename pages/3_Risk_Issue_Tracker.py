import streamlit as st
import pandas as pd
from datetime import datetime

def main():
    # Back button
    if st.button("← Back to Dashboard", key="back_submilestone"):
        st.switch_page("app.py")

    #st.title("Sub-Milestones Tracker")

    CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRtFXzX7qmZ2yyJPqnr8h_llta3uvIFnVsI0cwUWGMoZuJXPQ9c4Blm-WTFLVABWA/pub?gid=1934231119&single=true&output=csv"

    @st.cache_data(ttl=300)
    def load_data():
        df = pd.read_csv(CSV_URL)
        # Clean column names
        df.columns = df.columns.str.strip()
        # Replace empty with "NA"
        df = df.fillna("NA")
        df = df.replace("", "NA")
        df = df.replace(r"^\s*$", "NA", regex=True)
        
        # Desired columns in exact order
        desired_columns = ["Sub-Milestones", "Plan", "CWV", "CW", "Actual", "Remarks", "Lead time"]
        available_cols = [col for col in desired_columns if col in df.columns]
        df = df[available_cols]
        
        # Add missing columns
        for col in desired_columns:
            if col not in df.columns:
                df[col] = "NA"
        
        df = df[desired_columns]
        return df

    df = load_data()

    # Beautiful Header (Green like Milestone Tracker)
    st.markdown(f"""
    <div style="text-align:center; padding:20px; background:linear-gradient(135deg, #059669 0%, #10b981 100%); color:white; border-radius:16px; margin-bottom:30px; box-shadow: 0 12px 30px rgba(5,150,105,0.3);">
        <h1 style="margin:0; font-size:2.4rem; font-weight:800;">📋 DALLAS NA </h1>
        <p style="margin:10px 0 0 0; font-size:1.1rem;">
            Updated: {datetime.now().strftime('%d-%b-%Y %H:%M:%S')}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Two Large Metric Cards
    total_milestones = len(df)
    completed = len(df[df['Actual'] != "NA"])

    col_spacer1, col_total, col_spacer_mid, col_completed, col_spacer2 = st.columns([1.5, 5, 1, 5, 1.5])

    with col_total:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); color:white; padding:20px 40px; border-radius:16px; text-align:center; box-shadow:0 10px 25px rgba(59,130,246,0.4);">
            <p style="margin:0; font-size:1.2rem; font-weight:700;">📊 Total Sub-Milestones</p>
            <h2 style="margin:10px 0 0 0; font-size:4.2rem; font-weight:900;">{total_milestones}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col_completed:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg, #22c55e 0%, #16a34a 100%); color:white; padding:20px 40px; border-radius:16px; text-align:center; box-shadow:0 10px 25px rgba(34,197,94,0.4);">
            <p style="margin:0; font-size:1.2rem; font-weight:700;">✅ Completed</p>
            <h2 style="margin:10px 0 0 0; font-size:4.2rem; font-weight:900;">{completed}</h2>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Beautiful Table - No scroll, larger font, no pink triangles
    st.markdown("""
    <style>
        .big-font-table table {
            width: 100% !important;
            font-size: 18px !important;
            border-collapse: collapse;
        }
        .big-font-table td, .big-font-table th {
            padding: 14px !important;
            text-align: left !important;
            border: 1px solid #ddd !important;
            white-space: nowrap !important;
        }
        .big-font-table th {
            background: #1e40af !important;
            color: white !important;
            font-weight: bold !important;
        }
        .big-font-table tr:nth-child(even) {
            background-color: #f8fafc !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # HTML table with larger font and no horizontal scroll
    html = '<div class="big-font-table"><table><thead><tr>'
    for col in df.columns:
        html += f'<th>{col}</th>'
    html += '</tr></thead><tbody>'

    for _, row in df.iterrows():
        html += '<tr>'
        for val in row:
            html += f'<td>{val}</td>'
        html += '</tr>'

    html += '</tbody></table></div>'

    st.markdown(html, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.success("📋 DALLAS NA ")
        st.download_button(
            "📥 Download CSV",
            df.to_csv(index=False).encode(),
            "sub_milestones_data.csv",
            "text/csv"
        )

if __name__ == "__main__":
    main()