import streamlit as st
import pandas as pd
from sqlalchemy.orm import Session
from app.db import SessionLocal, engine
from app.models import Provider

# --- PAGE CONFIG ---
st.set_page_config(page_title="Provider Data Dashboard", layout="wide")

st.title("🏥 Provider Data Validation Dashboard")
st.markdown("Monitor provider data, confidence scores, and validation statuses in real time.")

# --- DATABASE ACCESS ---
session = SessionLocal()
providers = session.query(Provider).all()

# Convert SQLAlchemy objects → pandas DataFrame
data = [
    {
        "Name": p.full_name,
        "Phone": p.phone,
        "Email": p.email,
        "City": p.city,
        "State": p.state,
        "Specialty": p.specialty,
        "NPI Confidence": p.npi_confidence,
        "Address Confidence": p.address_confidence,
        "Validation Status": p.validation_status,
    }
    for p in providers
]
df = pd.DataFrame(data)

# --- FILTERS ---
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
avg_conf = df["NPI Confidence"].mean() if "NPI Confidence" in df else 0
col3.metric("Avg. NPI Confidence", f"{avg_conf:.2f}")

# --- DATA TABLE ---
st.dataframe(
    filtered_df,
    use_container_width=True,
    height=500,
)

# --- FOOTER ---
st.markdown("---")
st.caption("Built with ❤️ using Streamlit + SQLAlchemy + Faker")
