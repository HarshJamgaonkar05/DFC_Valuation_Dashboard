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
    ["Company Overview", "P&L & Revenue", "FCFF & Valuation", "WACC & DCF", "Ratios", "Balance Sheet"]
)

# -------------------- Company Overview Section --------------------
if section == "Company Overview":
    st.subheader(" About Titan Company")

    
    st.image("Assets/titan_logo.jpg", width=180) 

    
    try:
        titan_description_block = titan.iloc[4:15, 3]
        titan_description_text = "\n\n".join(titan_description_block.dropna().astype(str))
        st.markdown(titan_description_text)
    except Exception as e:
        st.warning(f"⚠️ Could not load company description: {e}")

    
    st.markdown(" Resources")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("[🔗 Screener.in - Titan](https://www.screener.in/company/TITAN/)")
        st.markdown("[🔗 Yahoo Finance - Titan](https://finance.yahoo.com/quote/TITAN.NS/)")


    st.markdown("---")
    

# -------------------- PNL SECTION --------------------
elif section == "P&L & Revenue":
    st.subheader(" Profit & Loss Statement")

    try:
        
        pnl_df = pd.read_excel(excel_path, sheet_name='Profit and Loss', header=2)

        
        pnl_df.dropna(axis=1, how='all', inplace=True)

        
        valid_rows_mask = pnl_df.iloc[:, 0].notna() & ~pnl_df.iloc[:, 0].astype(str).str.lower().str.contains(
        "assumption|remark|note|numerical|forecast|interest", na=False
                                                                    )
        pnl_df = pnl_df[valid_rows_mask].reset_index(drop=True)

        pnl_df.reset_index(drop=True, inplace=True)

        
        years = pnl_df.columns[1:]

       
        percentage_rows = [
            "EBITDA Margin(%)",
            "EBIT Margin(%)",
            "Net Profit Margin(%)",
            "Revenue Growth",
            "Tax Rate"
        ]

        
        for row_label in percentage_rows:
            mask = pnl_df.iloc[:, 0] == row_label
            if mask.any():
                pnl_df.loc[mask, years] = pnl_df.loc[mask, years].astype(float).applymap(
                    lambda x: f"{x * 100:.2f}%" if pd.notna(x) else ""
                )

        
        st.markdown("#### P&L Table")
        st.dataframe(pnl_df, use_container_width=True)

        
        with st.expander("Financial Trend Chart"):
            try:
                revenue = pnl_df[pnl_df[pnl_df.columns[0]] == "Revenue"].iloc[0, 1:]
                ebit = pnl_df[pnl_df[pnl_df.columns[0]] == "Operating Profit(EBIT)"].iloc[0, 1:]
                net_profit = pnl_df[pnl_df[pnl_df.columns[0]] == "Net Profit"].iloc[0, 1:]

                trend_df = pd.DataFrame({
                    "Year": years,
                    "Revenue (₹ Cr)": revenue.values.astype(float),
                    "EBIT (₹ Cr)": ebit.values.astype(float),
                    "Net Profit (₹ Cr)": net_profit.values.astype(float)
                }).set_index("Year")

                st.line_chart(trend_df)
            except Exception as plot_err:
                st.warning(f"Could not plot trends due to: {plot_err}")

        with st.expander(" Interpretation"):
            st.markdown("""
            - **Revenue** shows strong upward trajectory, indicating healthy top-line growth.
            - **EBIT** margin expansion reflects operating leverage and efficient management.
            - **Net Profit** increases steadily, affirming profitability and margin stability.
            """)

    except Exception as e:
        st.error(f"❌ Error processing P&L sheet: {e}")


# -------------------- FCFF & Valuation SECTION --------------------
elif section == "FCFF & Valuation":
    st.subheader(" Free Cash Flow to Firm (FCFF) Analysis")

    try:
        
        raw_fcff = pd.read_excel(excel_path, sheet_name='Free Cash Flow', header=2)

        
        fcff_df = raw_fcff.dropna(axis=1, how='all')

        
        fcff_df = fcff_df[fcff_df.iloc[:, 0].notna()]
        fcff_df.rename(columns={fcff_df.columns[0]: 'Metric'}, inplace=True)

        
        if fcff_df.shape[1] > 2:
            fcff_df = fcff_df.iloc[:, :-2]  

        
        years = fcff_df.columns[1:]  
        percent_rows = ["Tax Rate","FCFF Growth(%)"]  

        for label in percent_rows:
            mask = fcff_df['Metric'] == label
            if mask.any():
                fcff_df.loc[mask, years] = fcff_df.loc[mask, years].astype(float).applymap(
                    lambda x: f"{x * 100:.2f}%" if pd.notna(x) else ""
                )

        
        fcff_df.reset_index(drop=True, inplace=True)
        st.markdown("#### FCFF Table")
        st.dataframe(fcff_df.fillna(''), use_container_width=True)

        st.markdown("###  Interpretation & Insights")
        st.markdown("""
- **FCFF (Free Cash Flow to Firm)** reflects cash available to all capital providers after investments.
- Titan' FCFF fluctuates early on due to capex cycles but trends strongly positive from 2025.
- Positive FCFF supports Titan's valuation strength and signals strong reinvestment efficiency.
        """)

        st.markdown("### Formulae + Assumptions Behind FCFF Calculations")
        st.markdown("""
- **NOPAT** = EBIT x (1 - Tax Rate)  
- **CapEx** (2026-2030) = Assumed as 1.1% of forecasted revenue  
- **ΔWorking Capital** = Based on changes in operating assets & liabilities  
- **FCFF Formula Used**:  
  FCFF = NOPAT + Depreciation - CapEx - ΔWorking Capital
        """)

        st.markdown("---")

    except Exception as e:
        st.error(f" Error processing FCFF sheet: {e}")
