import time
from datetime import datetime
import streamlit as st
import pandas as pd
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Provider
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# --- PAGE CONFIG ---
st.set_page_config(page_title="Provider Data Dashboard", layout="wide")

# --- HEADER ---
st.title("🏥 Provider Data Validation Dashboard")
st.markdown("Monitor provider data accuracy, confidence levels, and validation progress — powered by Agentic AI.")

# --- EXPLANATION FOR NEW USERS ---
with st.expander("ℹ️ About this Dashboard (Read First)"):
    st.markdown("""
    This dashboard shows the results of **automated provider data validation** done by AI agents.

    **Status meanings:**
    - 🟢 **Validated** → Data confirmed accurate with high confidence (≥ 0.8)  
    - 🟡 **Review** → Partial or uncertain match (0.5 – 0.79) — needs manual review  
    - 🔴 **Pending** → Yet to be validated by any AI agent  

    **Confidence scores** show how certain the AI is about each validation result.
    """)

# --- AUTO REFRESH SETUP ---


REFRESH_INTERVAL = 10  # seconds
st_autorefresh(interval=REFRESH_INTERVAL * 1000, key="datarefresh")


# --- SHOW SPINNER DURING REFRESH ---
with st.spinner("🔄 Updating provider data..."):
    time.sleep(0.8)  # short delay just for animation

# --- LOAD DATABASE ---
session = SessionLocal()
providers = session.query(Provider).all()

data = []
for p in providers:
    # --- Weighted Confidence Logic ---
    npi_conf = p.npi_confidence or 0
    addr_conf = p.address_confidence or 0

    # Weighted combination (NPI = 70%, Address = 30%)
    total_conf = (0.7 * npi_conf) + (0.3 * addr_conf)

    # Assign status based on total confidence
    if total_conf >= 0.8:
        status = "validated"   # Strong across both or very high NPI match
    elif total_conf >= 0.5:
        status = "review"      # Partial match or one weak score
    else:
        status = "pending"     # No reliable validation yet

    data.append({
        "S.No": None,
        "Name": p.full_name,
        "Phone": p.phone,
        "Email": p.email,
        "City": p.city,
        "State": p.state,
        "Specialty": p.specialty,
        "NPI Confidence": round(npi_conf, 2) if npi_conf else None,
        "Address Confidence": round(addr_conf, 2) if addr_conf else None,
        "Validation Status": status,
    })

df = pd.DataFrame(data)
df["S.No"] = range(1, len(df) + 1)

if df.empty:
    st.warning("No provider data found! Please run the seeder and agents first.")
    st.stop()

# --- SIDEBAR FILTERS ---
st.sidebar.header("🔍 Filters")
status_filter = st.sidebar.multiselect(
    "Filter by Status",
    options=df["Validation Status"].dropna().unique(),
    default=list(df["Validation Status"].dropna().unique())
)
specialty_filter = st.sidebar.multiselect(
    "Filter by Specialty",
    options=df["Specialty"].dropna().unique(),
    default=list(df["Specialty"].dropna().unique())
)

filtered_df = df[
    (df["Validation Status"].isin(status_filter))
    & (df["Specialty"].isin(specialty_filter))
]

# --- METRICS ---
col1, col2, col3 = st.columns(3)
col1.metric("Total Providers", len(df))
col2.metric("Validated Providers", len(df[df["Validation Status"] == "validated"]))
avg_conf = df["NPI Confidence"].mean(skipna=True)
col3.metric("Avg. NPI Confidence", f"{avg_conf:.2f}")

# --- CONFIDENCE CHART ---
st.subheader("📊 Confidence Score Distribution")
fig = px.histogram(
    df,
    x="NPI Confidence",
    nbins=10,
    title="Distribution of NPI Confidence Scores",
    color_discrete_sequence=["#3b82f6"],
)
st.plotly_chart(fig, use_container_width=True)

# --- COLOR-CODED TABLE ---
def highlight_status(val):
    color_map = {
        "validated": "background-color: #d1fae5; color: #065f46;",   # green
        "review": "background-color: #fef9c3; color: #854d0e;",      # yellow
        "pending": "background-color: #fee2e2; color: #991b1b;",     # red
    }
    return color_map.get(val, "")

st.subheader("📋 Provider Records")
styled_df = filtered_df.style.applymap(highlight_status, subset=["Validation Status"])
st.dataframe(styled_df, use_container_width=True, height=600, hide_index=True)

# --- FOOTER ---
st.markdown("---")
last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.success(f"✅ Updated successfully at {last_updated}", icon="✅")
st.caption("Built with ❤️ using Streamlit | SQLAlchemy | Faker | Open Data APIs")
st.caption(f"🔁 Auto-refresh every {REFRESH_INTERVAL} seconds")
