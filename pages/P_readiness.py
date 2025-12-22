import streamlit as st
import pandas as pd
from datetime import datetime
import time

st.title("UTAH NA - Process Readiness Tracker")

REFRESH_INTERVAL = 30
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT3so_mMFyNEBJGBZuEYzTxaWDMSJg0nGznK4ln9r4i2OTRzL_AxATf8sSBgwEdfA/pub?gid=1714107674&single=true&output=csv"

@st.cache_data(ttl=REFRESH_INTERVAL)
def load_data():
    df = pd.read_csv(CSV_URL)
    df = df.dropna(how='all').reset_index(drop=True)
    df = df.fillna("—")
    df = df.loc[:, ~df.columns.duplicated()]
    return df

df = load_data()

# Header
st.markdown(f"""
<div style="text-align:center; padding:20px; background:linear-gradient(135deg, #1d4ed8 0%, #3b82f6 100%); color:white; border-radius:16px; margin-bottom:30px; box-shadow: 0 12px 30px rgba(29,78,216,0.3);">
    <h1 style="margin:0; font-size:2.4rem; font-weight:800;">UTAH NA</h1>
    <p style="margin:10px 0 0 0; font-size:1.1rem;">
        Updated: {datetime.now().strftime('%d-%b-%Y %H:%M:%S')} • Auto-refresh every {REFRESH_INTERVAL}s
    </p>
</div>
""", unsafe_allow_html=True)

# Column detection
category_col = next((c for c in df.columns if "process category" in c.lower()), df.columns[0])
sub_col = next((c for c in df.columns if "sub" in c.lower()), None)
owner_col = next((c for c in df.columns if "owner" in c.lower()), None)
target_col = next((c for c in df.columns if "target" in c.lower()), None)
status_col = next((c for c in df.columns if "status" in c.lower()), None)
remark_col = next((c for c in df.columns if "remark" in c.lower() or "remarks" in c.lower()), None)

# Status calculation
if target_col:
    df[target_col] = pd.to_datetime(df[target_col], errors='coerce', dayfirst=True)
today = pd.Timestamp('2025-12-22')  # As per current date

def get_final_status(row):
    closed = status_col and pd.notna(row.get(status_col)) and str(row[status_col]).strip().lower() in ["closed", "close", "done"]
    overdue = target_col and pd.notna(row.get(target_col)) and row[target_col].normalize() < today
    if closed and not overdue: return "Closed On Time"
    if closed and overdue: return "Closed (Late)"
    if overdue: return "NOT CLOSED – DELAYED!"
    return "Open"

df["Final Status"] = df.apply(get_final_status, axis=1)

# Metric Cards
delayed = len(df[df["Final Status"].str.contains("DELAYED")])
open_count = len(df[df["Final Status"] == "Open"])
closed = len(df[~df["Final Status"].str.contains("Open|DELAYED")])

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"<div style='background:#ef4444;color:white;padding:25px;border-radius:16px;text-align:center;box-shadow:0 10px 25px rgba(239,68,68,0.3);'><p style='margin:0;font-size:1.3rem;font-weight:700;'>Delayed</p><h2 style='margin:10px 0 0 0;'>{delayed}</h2></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div style='background:#fbbf24;color:white;padding:25px;border-radius:16px;text-align:center;box-shadow:0 10px 25px rgba(251,191,36,0.3);'><p style='margin:0;font-size:1.3rem;font-weight:700;'>Open</p><h2 style='margin:10px 0 0 0;'>{open_count}</h2></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div style='background:#22c55e;color:white;padding:25px;border-radius:16px;text-align:center;box-shadow:0 10px 25px rgba(34,197,94,0.3);'><p style='margin:0;font-size:1.3rem;font-weight:700;'>Closed</p><h2 style='margin:10px 0 0 0;'>{closed}</h2></div>", unsafe_allow_html=True)

st.markdown("---")

# Filters
col1, col2, col3 = st.columns(3)
filtered = df.copy()

with col1:
    if owner_col:
        owners = ["All"] + sorted(filtered[owner_col].dropna().unique().tolist())
        chosen_owner = st.selectbox("👤 Owner", owners, key="owner_ready")
        if chosen_owner != "All":
            filtered = filtered[filtered[owner_col] == chosen_owner]

with col2:
    categories = ["All"] + sorted(filtered[category_col].dropna().unique().tolist())
    chosen_cat = st.selectbox("📋 Process Category", categories, key="cat_ready")
    if chosen_cat != "All":
        filtered = filtered[filtered[category_col] == chosen_cat]

with col3:
    view = st.selectbox("🔍 View", ["All Items", "Only Delayed", "Only Open", "Only Closed"], key="view_ready")
    if view == "Only Delayed":
        filtered = filtered[filtered["Final Status"].str.contains("DELAYED")]
    elif view == "Only Open":
        filtered = filtered[filtered["Final Status"] == "Open"]
    elif view == "Only Closed":
        filtered = filtered[~filtered["Final Status"].str.contains("Open|DELAYED")]

# Alert
urgent = len(filtered[filtered["Final Status"].str.contains("DELAYED")])
if urgent:
    st.error(f"🚨 URGENT: {urgent} items DELAYED & NOT CLOSED!")
else:
    st.success("✅ All items are On Track or Closed")

# Table HTML
cols_to_show = [category_col, sub_col, owner_col, target_col, status_col, remark_col, "Final Status"]
valid_cols = [c for c in cols_to_show if c and c in filtered.columns]
table_df = filtered[valid_cols].reset_index(drop=True)

html = """
<div style="overflow-x:auto; margin:20px 0;">
<table style="width:100%; border-collapse:collapse; font-family:Arial, sans-serif;">
    <thead>
        <tr>
"""
for col in table_df.columns:
    html += f"<th style='background:#1e40af; color:white; padding:15px; text-align:left; font-weight:800;'>{col}</th>"
html += """
        </tr>
    </thead>
    <tbody>
"""

prev_cat = None
for _, row in table_df.iterrows():
    status = row["Final Status"]
    status_style = ""
    if "DELAYED" in status:
        status_style = "background:#ef4444; color:white; font-weight:bold;"
    elif "Late" in status:
        status_style = "background:#86efac; color:black; font-weight:bold;"
    elif "On Time" in status:
        status_style = "background:#22c55e; color:white; font-weight:bold;"
    elif status == "Open":
        status_style = "background:#fbbf24; color:black; font-weight:bold;"

    display_cat = "" if row[category_col] == prev_cat else row[category_col]
    prev_cat = row[category_col] if display_cat else prev_cat

    html += "<tr>"
    for col in table_df.columns:
        val = str(row[col])
        if col == category_col:
            cell_content = "" if val == prev_cat else val
        else:
            cell_content = val
        cell_style = status_style if col == "Final Status" else ""
        html += f"<td style='padding:12px; border:1px solid #ddd; {cell_style}'>{cell_content}</td>"
    html += "</tr>"

html += """
    </tbody>
</table>
</div>
"""

st.markdown(html, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.success("🎯 PROCESS READINESS TRACKER")
    st.download_button("📥 Download Current View", table_df.to_csv(index=False).encode(), "process_readiness.csv", "text/csv")

# Auto-refresh
time.sleep(REFRESH_INTERVAL)
st.rerun()