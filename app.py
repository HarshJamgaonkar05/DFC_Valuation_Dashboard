import streamlit as st
import pandas as pd
import os

# -------------------- Page Configuration --------------------
st.set_page_config(page_title="Titan DCF Valuation", layout="wide")
st.title("Titan Company DCF Valuation Dashboard")

# -------------------- Excel Loader with Cache --------------------
@st.cache_data
def load_excel_data(file_path):
    return pd.read_excel(file_path, sheet_name=None)

# -------------------- Load Excel File --------------------
excel_path = os.path.join("Data", "Final_Data.xlsx")
data = load_excel_data(excel_path)

# -------------------- Sheet Extraction --------------------
titan = pd.read_excel(excel_path, sheet_name='Titan', header=None)
pnl = pd.read_excel(excel_path, sheet_name='Profit and Loss', header=None)
fcff = pd.read_excel(excel_path, sheet_name='Free Cash Flow', header=None)
ratios = pd.read_excel(excel_path, sheet_name='Ratios', header=None)
balance_sheet = pd.read_excel(excel_path, sheet_name='Balance Sheet', header=None)
wacc = pd.read_excel(excel_path, sheet_name='WACC', header=None)
dcf = pd.read_excel(excel_path, sheet_name='DCF', header=None)


# -------------------- Sidebar Navigation --------------------
st.sidebar.title("Navigation")
section = st.sidebar.radio(
    "Go to section:",
    ["Company Overview", "P&L & Revenue", "FCFF & Valuation", "WACC", "Ratios", "Balance Sheet", "Assumptions"]
)

# -------------------- Company Overview Section --------------------
if section == "Company Overview":
    st.subheader(" About Titan Company")

    try:
        # Extract content from D5 (row index 4, col index 3)
        titan_description_block = titan.iloc[4:15, 3]
        titan_description_text = "\n".join(titan_description_block.dropna().astype(str))
        st.markdown(titan_description_text)
    except Exception as e:
        st.warning(f"⚠️ Could not load description: {e}")

    st.markdown("---")
