import streamlit as st
import pandas as pd
from datetime import datetime
import time

st.set_page_config(page_title="Project Trackers", layout="wide")

# --------------------- CONFIG ---------------------
REFRESH_READINESS = 30
REFRESH_MILESTONE = 60

CSV_READINESS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT3so_mMFyNEBJGBZuEYzTxaWDMSJg0nGznK4ln9r4i2OTRzL_AxATf8sSBgwEdfA/pub?gid=1714107674&single=true&output=csv"
CSV_MILESTONE = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSERW8jK8wY8-01wqcDBtNY_g8Km2g3QyxNjT1BWIg2II95wvouLQ1wsgWckkY56Q/pub?gid=1960938483&single=true&output=csv"

# --------------------- DATA LOADING ---------------------
@st.cache_data(ttl=REFRESH_READINESS)
def load_readiness_data():
    try:
        df = pd.read_csv(CSV_READINESS)
        df = df.dropna(how='all').reset_index(drop=True)
        df = df.fillna("—")
        df = df.loc[:, ~df.columns.duplicated()]
        return df
    except Exception as e:
        st.error(f"Readiness data load error: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=REFRESH_MILESTONE)
def load_milestone_data():
    try:
        df = pd.read_csv(CSV_MILESTONE, header=None)
        df = df.iloc[1:]
        df = df[[0,1,2,3]]
        df.columns = ["Task", "Milestone_Type", "Plan_Date", "Actual_Date"]
        df = df.fillna("—")
        df = df.reset_index(drop=True)
        return df
    except Exception as e:
        st.error(f"Milestone data load error: {e}")
        return pd.DataFrame()

# --------------------- THEME-AWARE CSS FIX ---------------------
# Detect current theme
theme = st.get_option("theme.base")
is_dark = theme == "dark"

# Dynamic text color for normal cells
normal_text_color = "white" if is_dark else "black"

st.markdown(f"""
<style>
/* Full text visibility + wrapping */
.scrollable-table {{
    overflow-x: auto !important;
    width: 100% !important;
    margin-bottom: 20px;
    padding: 1px;
}}

.stMarkdown table {{
    width: 100% !important;
    min-width: 900px !important;
    table-layout: auto !important;
    border-collapse: collapse !important;
    font-family: Arial, sans-serif !important;
}}

.stMarkdown table td, .stMarkdown table th {{
    white-space: normal !important;
    word-wrap: break-word !important;
    padding: 12px !important;
    border: 1px solid #ccc !important;
    min-width: 140px !important;
    text-align: left !important;
    vertical-align: top !important;
}}

/* Header */
.stMarkdown table th {{
    background: #1e40af !important;
    color: white !important;
    position: sticky !important;
    top: 0 !important;
    z-index: 2 !important;
    font-weight: bold !important;
}}

/* Normal cell text color - adapts to theme */
.stMarkdown table td {{
    color: {normal_text_color} !important;
    font-weight: bold !important;
}}

/* Status column overrides - high contrast */
.status-delayed, .status-overdue {{
    background: #ef4444 !important;
    color: white !important;
    font-weight: bold !important;
}}
.status-closed-ontime {{
    background: #22c55e !important;
    color: white !important;
    font-weight: bold !important;
}}
.status-closed-late {{
    background: #86efac !important;
    color: black !important;
    font-weight: bold !important;
}}
.status-open, .status-pending {{
    background: #fbbf24 !important;
    color: black !important;
    font-weight: bold !important;
}}
</style>
""", unsafe_allow_html=True)

# --------------------- HOME PAGE ---------------------
st.markdown("<h1 style='text-align: center;'>🚀 Trackers Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Select one of the trackers below by clicking the card.</p>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    if st.button("**Process Readiness Tracker**", use_container_width=True, type="primary" if st.session_state.get('page', 'readiness') != "milestone" else "secondary"):
        st.session_state.page = "readiness"
        st.rerun()
with col2:
    if st.button("**Milestone Tracker Dashboard**", use_container_width=True, type="primary" if st.session_state.get('page') == "milestone" else "secondary"):
        st.session_state.page = "milestone"
        st.rerun()

if "page" not in st.session_state:
    st.session_state.page = "readiness"

# --------------------- PROCESS READINESS TRACKER ---------------------
if st.session_state.page == "readiness":
    placeholder = st.empty()
    while True:
        df = load_readiness_data()
        with placeholder.container():
            if df.empty:
                st.warning("No readiness data loaded.")
                time.sleep(REFRESH_READINESS)
                st.rerun()

            st.markdown(f"""
            <div style="text-align:center; padding:15px; background:#1d4ed8; color:white; border-radius:8px; margin-bottom:20px;">
                <h1 style="margin:0; font-size:1.8rem;">UTAH NA</h1>
                <p style="margin:5px 0 0 0; font-size:0.9rem;">
                    Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} • Auto-refresh {REFRESH_READINESS}s
                </p>
            </div>
            """, unsafe_allow_html=True)

            # Column detection
            category_col = next((c for c in df.columns if "process category" in c.lower()), df.columns[0])
            sub_col = next((c for c in df.columns if "sub" in c.lower()), None)
            owner_col = next((c for c in df.columns if "owner" in c.lower()), None)
            target_col = next((c for c in df.columns if "target" in c.lower()), None)
            status_col = next((c for c in df.columns if "status" in c.lower()), None)
            remark_col = next((c for c in df.columns if "remark" in c.lower()), None)

            if target_col:
                df[target_col] = pd.to_datetime(df[target_col], errors='coerce', dayfirst=True)
            today = pd.Timestamp.today().normalize()

            def get_status(row):
                closed = status_col and str(row[status_col]).strip().lower() in ["closed", "close", "done"]
                overdue = target_col and pd.notna(row[target_col]) and row[target_col].normalize() < today
                if closed and not overdue: return "Closed On Time"
                if closed and overdue: return "Closed (Late)"
                if overdue: return "NOT CLOSED – DELAYED!"
                return "Open"
            df["Final Status"] = df.apply(get_status, axis=1)

            # Metrics
            delayed_count = len(df[df["Final Status"].str.contains("DELAYED")])
            open_count = len(df[df["Final Status"] == "Open"])
            closed_count = len(df[~df["Final Status"].str.contains("Open|DELAYED")])

            m1, m2, m3 = st.columns(3)
            with m1: st.markdown(f"<div style='background:#ef4444;color:white;padding:15px;border-radius:8px;text-align:center;'><p style='margin:0;font-weight:bold;'>Delayed</p><h2>{delayed_count}</h2></div>", unsafe_allow_html=True)
            with m2: st.markdown(f"<div style='background:#fbbf24;color:black;padding:15px;border-radius:8px;text-align:center;'><p style='margin:0;font-weight:bold;'>Open</p><h2>{open_count}</h2></div>", unsafe_allow_html=True)
            with m3: st.markdown(f"<div style='background:#22c55e;color:white;padding:15px;border-radius:8px;text-align:center;'><p style='margin:0;font-weight:bold;'>Closed</p><h2>{closed_count}</h2></div>", unsafe_allow_html=True)

            # Filters
            colf1, colf2, colf3 = st.columns(3)
            filtered = df.copy()
            with colf1:
                if owner_col:
                    owners = ["All"] + sorted(filtered[owner_col].dropna().unique().tolist())
                    chosen_owner = st.selectbox("Owner", owners, key="owner_r")
                    if chosen_owner != "All": filtered = filtered[filtered[owner_col] == chosen_owner]
            with colf2:
                if category_col:
                    cats = ["All"] + sorted(filtered[category_col].dropna().unique().tolist())
                    chosen_cat = st.selectbox("Process Category", cats, key="cat_r")
                    if chosen_cat != "All": filtered = filtered[filtered[category_col] == chosen_cat]
            with colf3:
                view = st.selectbox("Show", ["All Items", "Only Delayed", "Only Open", "Only Closed"], key="view_r")
                if view == "Only Delayed": filtered = filtered[filtered["Final Status"].str.contains("DELAYED")]
                elif view == "Only Open": filtered = filtered[filtered["Final Status"] == "Open"]
                elif view == "Only Closed": filtered = filtered[~filtered["Final Status"].str.contains("Open|DELAYED")]

            urgent_count = len(filtered[filtered["Final Status"].str.contains("DELAYED")])
            if urgent_count:
                st.error(f"URGENT: {urgent_count} items DELAYED & NOT CLOSED!")
            else:
                st.success("All items are On Track or Closed")

            # Table
            cols_to_show = [category_col, sub_col, owner_col, target_col, status_col, remark_col, "Final Status"]
            valid_cols = [c for c in cols_to_show if c and c in filtered.columns]
            table_df = filtered[valid_cols].reset_index(drop=True)

            html = ['<div class="scrollable-table">']
            html.append('<table><tr>' + ''.join(f'<th>{c}</th>' for c in table_df.columns) + '</tr>')

            prev_cat = None
            for _, row in table_df.iterrows():
                status = row["Final Status"]
                status_class = ("status-delayed" if "DELAYED" in status else
                                "status-closed-late" if "Late" in status else
                                "status-closed-ontime" if "On Time" in status else
                                "status-open" if status == "Open" else "")

                cells = []
                for col in table_df.columns:
                    val = str(row[col])
                    display_val = "" if col == category_col and val == prev_cat else val
                    if col == category_col and val != prev_cat:
                        prev_cat = val

                    cell_attr = f'class="{status_class}"' if col == "Final Status" else ''
                    cells.append(f'<td {cell_attr}>{display_val}</td>')
                html.append('<tr>' + ''.join(cells) + '</tr>')
            html.append('</table></div>')
            st.markdown(''.join(html), unsafe_allow_html=True)

            st.sidebar.success("PROCESS READINESS • THEME-ADAPTIVE TEXT")
            st.sidebar.download_button("Download View", table_df.to_csv(index=False).encode(), "Readiness_View.csv", "text/csv")

        time.sleep(REFRESH_READINESS)
        st.rerun()

# --------------------- MILESTONE TRACKER ---------------------
elif st.session_state.page == "milestone":
    placeholder = st.empty()
    while True:
        df = load_milestone_data()
        with placeholder.container():
            if df.empty:
                st.warning("No milestone data loaded.")
                time.sleep(REFRESH_MILESTONE)
                st.rerun()

            current_year = datetime.now().year
            def parse_date(val):
                if pd.isna(val) or val == "—" or str(val).strip() == "": return pd.NaT
                s = str(val).strip()
                if '-' in s and len(s.split('-')) == 2:
                    s = s + f"-{current_year}"
                return pd.to_datetime(s, dayfirst=True, errors='coerce')

            df['Plan_Date'] = df['Plan_Date'].apply(parse_date)
            df['Actual_Date'] = df['Actual_Date'].apply(parse_date)
            today = pd.Timestamp.today().normalize()

            def get_status(row):
                actual = row['Actual_Date']
                plan = row['Plan_Date']
                if pd.notna(actual):
                    return "Completed On Time" if pd.notna(plan) and actual <= plan else "Delayed"
                elif pd.notna(plan) and plan < today:
                    return "Overdue (No Actual)"
                else:
                    return "Pending"
            df['Status'] = df.apply(get_status, axis=1)

            st.markdown("### 📋 Milestone Tracker Dashboard")
            st.caption(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} • Auto-refresh {REFRESH_MILESTONE}s")

            chosen_type = st.selectbox("Filter by Milestone Type", ["All", "WBS", "Sub Milestone"], key="mil_f")
            filtered = df.copy()
            if chosen_type != "All":
                filtered = filtered[filtered["Milestone_Type"] == chosen_type]

            delayed_count = len(filtered[filtered['Status'].str.contains("Delayed|Overdue")])
            if delayed_count:
                st.error(f"URGENT: {delayed_count} milestones DELAYED or OVERDUE!")
            else:
                st.success("All milestones are on track")

            table_df = filtered[["Task", "Milestone_Type", "Plan_Date", "Actual_Date", "Status"]].copy()
            table_df['Plan_Date'] = table_df['Plan_Date'].dt.strftime('%d-%b').fillna("—")
            table_df['Actual_Date'] = table_df['Actual_Date'].dt.strftime('%d-%b').fillna("—")

            html = ['<div class="scrollable-table">']
            html.append('<table><tr>' + ''.join(f'<th>{col}</th>' for col in table_df.columns) + '</tr>')

            prev_task = None
            for _, row in table_df.iterrows():
                status = row['Status']
                status_class = ("status-delayed" if "Delayed" in status or "Overdue" in status else
                                "status-closed-ontime" if "On Time" in status else
                                "status-pending" if "Pending" in status else "")

                display_task = "" if row['Task'] == prev_task else row['Task']
                prev_task = row['Task']

                cells = []
                for col_name, val in zip(table_df.columns, row):
                    display_val = display_task if col_name == "Task" else val
                    cell_attr = f'class="{status_class}"' if col_name == "Status" else ''
                    cells.append(f'<td {cell_attr}>{display_val}</td>')
                html.append('<tr>' + ''.join(cells) + '</tr>')
            html.append('</table></div>')
            st.markdown(''.join(html), unsafe_allow_html=True)

            st.sidebar.success("MILESTONE TRACKER • THEME-ADAPTIVE TEXT")
            st.sidebar.download_button("Download View", table_df.to_csv(index=False).encode(), "Milestones_View.csv", "text/csv")

        time.sleep(REFRESH_MILESTONE)
        st.rerun()