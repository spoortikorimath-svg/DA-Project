"""
app.py
------
Local web app (Streamlit) — Cloud Infrastructure Usage & Cost Analytics.

Run:  streamlit run app.py
Then open the localhost URL it prints (usually http://localhost:8501).

New in this version:
- Password login screen (password lives in .streamlit/secrets.toml, not
  in this file) — the app won't show anything until the right password
  is entered.
- New color theme (teal/emerald — see .streamlit/config.toml).
- An "Overview" tab that loads FIRST with a high-level summary, before
  the detailed filterable dashboard (now on a second tab).
"""

import streamlit as st
import matplotlib.pyplot as plt
from analysis import (
    load_data, total_cost, cost_by_category, category_cost,
    data_transfer_total_gb, service_analysis, region_analysis,
    department_analysis, environment_analysis, monthly_cost,
    top_accounts, detect_anomalies,
)

st.set_page_config(page_title="Cloud Infra Cost Analytics", layout="wide", page_icon="☁️")

# ---------------------------------------------------------------------
# COLORS — change these to restyle the whole app in one place.
# (Also update .streamlit/config.toml to match the overall theme.)
# ---------------------------------------------------------------------
ACCENT = "#14B8A6"        # teal — buttons, active widgets, links
CHART_COLORS = ["#14B8A6", "#F59E0B", "#8B5CF6", "#38BDF8", "#F43F5E", "#84CC16"]
CARD_BG = "#111827"
TEXT_COLOR = "#E5E7EB"

st.markdown(f"""
<style>
    /* Whole app background stays dark even outside the main content box */
    .stApp {{
        background-color: #0B1220;
    }}

    /* ALL buttons everywhere — normal buttons, download button, AND the
       login form's submit button — styled the same dark-theme way */
    .stButton>button,
    .stDownloadButton>button,
    div[data-testid="stFormSubmitButton"]>button {{
        background-color: {ACCENT};
        color: #0B1220;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1.2rem;
        font-weight: 700;
        width: 100%;
        transition: 0.2s;
    }}
    .stButton>button:hover,
    .stDownloadButton>button:hover,
    div[data-testid="stFormSubmitButton"]>button:hover {{
        background-color: #0D9488;
        color: white;
        border: none;
    }}

    div[data-testid="stMetric"] {{
        background-color: {CARD_BG};
        border-radius: 10px;
        padding: 12px 16px;
        border: 1px solid #1F2937;
    }}
    div[data-testid="stMetricValue"] {{
        color: {ACCENT};
    }}
    h1, h2, h3 {{
        color: {TEXT_COLOR};
    }}
    .stTabs [data-baseweb="tab"] {{
        font-weight: 600;
    }}

    /* Login front-page card */
    .login-card {{
        background-color: {CARD_BG};
        border: 1px solid #1F2937;
        border-radius: 16px;
        padding: 40px 36px 28px 36px;
        margin-top: 60px;
        text-align: center;
        box-shadow: 0 8px 30px rgba(0,0,0,0.4);
    }}
    .login-icon {{
        font-size: 48px;
    }}
    .login-title {{
        color: {TEXT_COLOR};
        font-size: 26px;
        font-weight: 700;
        margin: 6px 0 2px 0;
    }}
    .login-sub {{
        color: #9CA3AF;
        font-size: 14px;
        margin-bottom: 22px;
    }}
    .login-footer {{
        color: #6B7280;
        font-size: 12px;
        margin-top: 18px;
    }}
</style>
""", unsafe_allow_html=True)

plt.style.use("dark_background")


# =======================================================================
# MAIN APP — password login removed, opens straight to the dashboard
# =======================================================================
st.title("☁️ Cloud Infrastructure Usage & Cost Analytics")

df = load_data()
min_date = df["Usage Date"].min().date()
max_date = df["Usage Date"].max().date()


def show_fig(fig):
    """Render a Matplotlib figure and close it immediately after, so
    figures don't pile up in memory and slow the app down."""
    st.pyplot(fig)
    plt.close(fig)


tab_overview, tab_detail = st.tabs(["🏠 Overview", "📊 Detailed Analysis"])

# -----------------------------------------------------------------------
# TAB 1 — OVERVIEW (loads first, whole dataset, no filters — a quick
# company-wide snapshot before drilling into details)
# -----------------------------------------------------------------------
with tab_overview:
    st.subheader("Company-Wide Snapshot")
    st.caption(f"All data · {min_date} to {max_date}")

    o1, o2, o3, o4 = st.columns(4)
    o1.metric("Total Cloud Cost", f"${total_cost(df):,.2f}")
    o2.metric("Compute Cost", f"${category_cost(df, 'Compute'):,.2f}")
    o3.metric("Storage Cost", f"${category_cost(df, 'Storage'):,.2f}")
    o4.metric("Data Transfer", f"{data_transfer_total_gb(df):,.1f} GB")

    st.markdown("#### Monthly Cost Trend")
    m = monthly_cost(df)
    fig, ax = plt.subplots(figsize=(10, 3.2))
    ax.plot(m["Month"], m["Cost"], marker="o", color=ACCENT, linewidth=2)
    ax.fill_between(range(len(m)), m["Cost"], color=ACCENT, alpha=0.15)
    ax.set_ylabel("Cost (USD)")
    ax.tick_params(axis="x", rotation=45)
    show_fig(fig)

    o5, o6 = st.columns(2)
    with o5:
        st.markdown("#### Top 5 Departments")
        dept = department_analysis(df).head(5)
        fig, ax = plt.subplots(figsize=(5, 3.5))
        ax.barh(dept["Department"], dept["Cost"], color=ACCENT)
        ax.invert_yaxis()
        ax.set_xlabel("Cost (USD)")
        show_fig(fig)
    with o6:
        st.markdown("#### Top 5 Services")
        svc = service_analysis(df).head(5)
        fig, ax = plt.subplots(figsize=(5, 3.5))
        ax.barh(svc["Service"], svc["Cost"], color=CHART_COLORS[1])
        ax.invert_yaxis()
        ax.set_xlabel("Cost (USD)")
        show_fig(fig)

    st.info("Switch to **📊 Detailed Analysis** to filter by region, department, environment, and date range.")

# -----------------------------------------------------------------------
# TAB 2 — DETAILED ANALYSIS (filterable, everything from before)
# -----------------------------------------------------------------------
with tab_detail:
    st.sidebar.header("Filters")
    regions = st.sidebar.multiselect(
        "Region", sorted(df["Region"].unique()), default=sorted(df["Region"].unique()), key="f_region"
    )
    departments = st.sidebar.multiselect(
        "Department", sorted(df["Department"].unique()), default=sorted(df["Department"].unique()), key="f_dept"
    )
    environments = st.sidebar.multiselect(
        "Environment", sorted(df["Environment"].unique()), default=sorted(df["Environment"].unique()), key="f_env"
    )
    date_range = st.sidebar.date_input(
        "Usage Date range", value=(min_date, max_date),
        min_value=min_date, max_value=max_date, key="f_date",
    )
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = min_date, max_date

    if st.sidebar.button("Reset filters", key="reset_btn"):
        st.rerun()

    mask = (
        df["Region"].isin(regions)
        & df["Department"].isin(departments)
        & df["Environment"].isin(environments)
        & (df["Usage Date"].dt.date >= start_date)
        & (df["Usage Date"].dt.date <= end_date)
    )
    fdf = df[mask]

    if fdf.empty:
        st.warning("No data matches the selected filters. Try widening your date range or filters.")
        st.stop()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Cloud Cost", f"${total_cost(fdf):,.2f}")
    c2.metric("Compute Cost", f"${category_cost(fdf, 'Compute'):,.2f}")
    c3.metric("Storage Cost", f"${category_cost(fdf, 'Storage'):,.2f}")
    c4.metric("Data Transfer", f"{data_transfer_total_gb(fdf):,.1f} GB")

    c5, c6 = st.columns(2)
    c5.metric("Database Cost", f"${category_cost(fdf, 'Database'):,.2f}")
    c6.metric("Network Cost", f"${category_cost(fdf, 'Network'):,.2f}")

    st.divider()

    c7, c8 = st.columns((2, 1))
    with c7:
        st.subheader("Monthly Cloud Cost")
        m = monthly_cost(fdf)
        fig, ax = plt.subplots(figsize=(8, 3.2))
        ax.plot(m["Month"], m["Cost"], marker="o", color=ACCENT)
        ax.set_ylabel("Cost (USD)")
        ax.tick_params(axis="x", rotation=45)
        show_fig(fig)
    with c8:
        st.subheader("Cost by Category")
        cat = cost_by_category(fdf)
        fig, ax = plt.subplots(figsize=(4, 3.2))
        ax.bar(cat["Category"], cat["Cost"], color=CHART_COLORS[:len(cat)])
        ax.set_ylabel("Cost (USD)")
        ax.tick_params(axis="x", rotation=20)
        show_fig(fig)

    c9, c10 = st.columns(2)
    with c9:
        st.subheader("Service Analysis")
        svc = service_analysis(fdf)
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.barh(svc["Service"], svc["Cost"], color=ACCENT)
        ax.invert_yaxis()
        ax.set_xlabel("Cost (USD)")
        show_fig(fig)
    with c10:
        st.subheader("Region Analysis")
        reg = region_analysis(fdf)
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(reg["Region"], reg["Cost"], color=CHART_COLORS[3])
        ax.set_ylabel("Cost (USD)")
        ax.tick_params(axis="x", rotation=30)
        show_fig(fig)

    c11, c12 = st.columns(2)
    with c11:
        st.subheader("Department Analysis")
        dept = department_analysis(fdf)
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.pie(dept["Cost"], labels=dept["Department"], autopct="%1.0f%%",
               startangle=90, colors=CHART_COLORS)
        show_fig(fig)
    with c12:
        st.subheader("Environment Split")
        env = environment_analysis(fdf)
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.bar(env["Environment"], env["Cost"], color=[CHART_COLORS[2], CHART_COLORS[5], CHART_COLORS[4]])
        ax.set_ylabel("Cost (USD)")
        show_fig(fig)

    st.divider()

    c13, c14 = st.columns((1, 2))
    with c13:
        st.subheader("Top 10 Accounts by Cost")
        st.dataframe(top_accounts(fdf), use_container_width=True, hide_index=True)
    with c14:
        st.subheader("⚠️ Detected Cost Anomalies")
        anomalies = detect_anomalies(fdf)
        if anomalies.empty:
            st.success("No unusual cost spikes detected in this range.")
        else:
            st.dataframe(anomalies, use_container_width=True, hide_index=True)

    st.divider()

    st.subheader("Export for Power BI")
    st.write("Download the filtered dataset, then load it into Power BI via **Get Data → Text/CSV**.")
    st.download_button(
        "⬇️ Download filtered data as CSV",
        data=fdf.drop(columns=["Category"]).to_csv(index=False).encode("utf-8"),
        file_name="cloud_infra_usage_cost_filtered.csv",
        mime="text/csv",
        key="download_btn",
    )

    with st.expander("View raw filtered data"):
        st.dataframe(fdf, use_container_width=True, hide_index=True)
