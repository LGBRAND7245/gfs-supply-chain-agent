
import streamlit as st
import pandas as pd

# --- Password Gate ---
st.set_page_config(page_title="Supply Chain Agent", layout="wide")
password = st.secrets.get("app_password")
input_pass = st.text_input("Enter app password:", type="password")
if input_pass != password:
    st.stop()

st.title("📦 GFS Supply Chain AI Agent")

# Load Excel
@st.cache_data
def load_data():
    df = pd.read_excel("Roosters CDV Tracker (2025-02-12) (1).xlsx", sheet_name="Sheet1")
    df = df[[
        'Material', 'Description', 'Chain Specialist Comments', 'Replenishment Planner Comments',
        'Purchasing Status', 'Days Of Coverage', 'Percent Of Sales',
        'FCST: Current Week - HIST: Last Week', 'Total FCST Error', 'FCST Accuracy'
    ]].rename(columns={
        'Material': 'SKU',
        'Description': 'Product Description',
        'Chain Specialist Comments': 'Specialist Notes',
        'Replenishment Planner Comments': 'Planner Notes',
        'Purchasing Status': 'Status',
        'Days Of Coverage': 'Coverage Days',
        'Percent Of Sales': 'Sales Share',
        'FCST: Current Week - HIST: Last Week': 'Forecast Delta',
        'Total FCST Error': 'Forecast Error',
        'FCST Accuracy': 'Forecast Accuracy'
    }).dropna(subset=["SKU"])
    return df
    )

df = load_data()
sku_search = st.text_input("Search by SKU or keyword:")

if sku_search:
    results = df[df.apply(lambda row: sku_search.lower() in str(row).lower(), axis=1)]
else:
    results = df.copy()

st.write(f"Showing {len(results)} result(s)")
for _, row in results.iterrows():
    st.markdown("---")
    st.markdown(summarize_row(row))

# Show insights
st.markdown("## 🔍 AI Insights")
if st.button("Show SKUs Out of Stock Due to Overforecasting"):
    filtered = df[
        (df["Coverage Days"] == 0) & 
        (df["Planner Notes"].str.contains("overforecast", case=False, na=False))
    ]
    if filtered.empty:
        st.info("No SKUs match that criteria.")
    else:
        for _, row in filtered.iterrows():
            st.markdown("---")
            st.markdown(summarize_row(row))
