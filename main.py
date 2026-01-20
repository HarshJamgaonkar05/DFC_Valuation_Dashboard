import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configure page
st.set_page_config(
    page_title="Titan Company DCF Valuation",
    page_icon="Assets\Titan_logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .header {font-family: 'Arial', sans-serif; color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px}
    .metric-card {background-color: #f8f9fa; border-radius: 10px; padding: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px}
    .metric-title {font-size: 14px; color: #7f8c8d; margin-bottom: 5px}
    .metric-value {font-size: 24px; font-weight: 700; color: #2c3e50}
    .metric-sub {font-size: 12px; color: #95a5a6}
    .section-title {font-size: 20px; font-weight: 700; color: #2c3e50; margin: 25px 0 15px 0; padding-bottom: 8px; border-bottom: 1px solid #ecf0f1}
    .stDataFrame {border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1)}
</style>
""", unsafe_allow_html=True)

# Sidebar with key inputs
with st.sidebar:
    st.title("DCF Parameters")
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("WACC", "8.55%")
    with col2:
        st.metric("Terminal Growth", "5.0%")
        
    st.divider()
    st.subheader("Key Assumptions")
    st.markdown("- Depreciation at 1.1% of revenue")
    st.markdown("- Tax rate fixed at 25% for forecast years")
    st.markdown("- Debt reduction: ₹1,000 Cr/year")
    st.markdown("- Equity Share Capital is assumed constant at ₹89 Cr")
    st.markdown("- Borrowings are forecasted with a ₹1,000 Cr annual decline for forecast years")
    st.markdown("- Forecasted CapEx is assumed to be 2% of forecasted revenue")
    
    st.divider()
    st.caption("Valuation by Harsh Jamgaonkar (IIT Gandhinagar) - 23110130")
    st.caption("Data Sources: Screener.in, Yahoo Finance")

# Main content
st.title("Titan Company DCF Valuation")
st.markdown("**Flagship enterprise of Tata Group** • Founded in 1984 • Bengaluru HQ • Jewelry, Watches, Eyewear")

# Key metrics at top (all values from Excel)
col1, col2, col3, col4 = st.columns(4)
col1.markdown('<div class="metric-card"><div class="metric-title">Enterprise Value</div><div class="metric-value">₹2,83,867.75 Cr</div><div class="metric-sub">Market Cap: ₹3,25,480 Cr</div></div>', unsafe_allow_html=True)
col2.markdown('<div class="metric-card"><div class="metric-title">Intrinsic Share Price</div><div class="metric-value">₹3,038.66</div><div class="metric-sub">Current: ₹3,666</div></div>', unsafe_allow_html=True)
col3.markdown('<div class="metric-card"><div class="metric-title">Revenue (FY2025)</div><div class="metric-value">₹60,456 Cr</div><div class="metric-sub">5-Year CAGR: 23.5%</div></div>', unsafe_allow_html=True)
col4.markdown('<div class="metric-card"><div class="metric-title">Net Profit (FY2025)</div><div class="metric-value">₹3,337 Cr</div><div class="metric-sub">Margin: 5.52%</div></div>', unsafe_allow_html=True)

# Revenue and Profit Charts (values directly from Revenue and P&L sheets)
st.markdown('<div class="section-title">Financial Performance</div>', unsafe_allow_html=True)

# Prepare data (directly from Excel)
years = [2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030]
revenue = [21052, 21644, 28799, 40575, 51084, 60456, 75087, 90593, 106086, 120462, 132508]
ebit = [2463, 1725, 3344, 4882, 5292, 5694, 8935, 11233, 13685, 15539, 17093]
net_profit = [1493, 974, 2198, 3274, 3496, 3337, 6026, 7750, 9588, 10979, 12145]

# Create dataframe
financial_df = pd.DataFrame({
    'Year': years,
    'Revenue': revenue,
    'EBIT': ebit,
    'Net Profit': net_profit
})

# Create charts
fig = make_subplots(rows=1, cols=2, specs=[[{"type": "bar"}, {"type": "scatter"}]])
fig.add_trace(go.Bar(x=years, y=revenue, name='Revenue', marker_color='#3498db'), row=1, col=1)
fig.add_trace(go.Scatter(x=years, y=ebit, name='EBIT', mode='lines+markers', line=dict(color='#e74c3c', width=3)), row=1, col=2)
fig.add_trace(go.Scatter(x=years, y=net_profit, name='Net Profit', mode='lines+markers', line=dict(color='#27ae60', width=3)), row=1, col=2)

# Update layout
fig.update_layout(
    height=400,
    margin=dict(l=20, r=20, t=40, b=20),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    plot_bgcolor='rgba(0,0,0,0)'
)

fig.update_yaxes(title_text="₹ Crores", row=1, col=1)
fig.update_yaxes(title_text="₹ Crores", row=1, col=2)
fig.update_xaxes(title_text="Year", row=1, col=1)
fig.update_xaxes(title_text="Year", row=1, col=2)

st.plotly_chart(fig, use_container_width=True)

# Margins and Ratios (calculated from P&L and Balance Sheet)
st.markdown('<div class="section-title">Profitability Metrics</div>', unsafe_allow_html=True)

# Margin data (calculated from Excel values)
# EBIT Margin = EBIT / Revenue
ebit_margin = [round(ebit[i]/revenue[i]*100, 2) for i in range(len(years))]
# Net Margin = Net Profit / Revenue
net_margin = [round(net_profit[i]/revenue[i]*100, 2) for i in range(len(years))]
# ROE values from Ratios sheet
roe = [22.39, 12.99, 23.63, 27.63, 37.22, 28.71, 34.14, 30.51, 27.40, 23.88, 20.90]

margin_df = pd.DataFrame({
    'Year': years,
    'EBIT Margin (%)': ebit_margin,
    'Net Margin (%)': net_margin,
    'ROE (%)': roe
})

# Create margin chart
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=years, y=ebit_margin, name='EBIT Margin', mode='lines+markers', line=dict(color='#3498db', width=3)))
fig2.add_trace(go.Scatter(x=years, y=net_margin, name='Net Margin', mode='lines+markers', line=dict(color='#e74c3c', width=3)))
fig2.add_trace(go.Scatter(x=years, y=roe, name='ROE', mode='lines+markers', line=dict(color='#27ae60', width=3)))

fig2.update_layout(
    height=300,
    margin=dict(l=20, r=20, t=30, b=20),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis_title="Percentage (%)"
)

st.plotly_chart(fig2, use_container_width=True)

# Valuation and Cash Flow (from DCF and Free Cash Flow sheets)
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="section-title">DCF Valuation Breakdown</div>', unsafe_allow_html=True)
    
    # DCF components (from DCF sheet)
    components = {
        'Component': ['Terminal Value', 'Enterprise Value', 'Net Debt', 'Equity Value'],
        'Value (₹ Cr)': [385728.07, 283867.75, 14248, 269620.25]
    }
    dcf_df = pd.DataFrame(components)
    
    
    # Format for display
    dcf_display = dcf_df.copy()
    dcf_display['Value (₹ Cr)'] = dcf_display['Value (₹ Cr)'].apply(lambda x: f'₹{x:,.0f}')
    
    
    st.dataframe(
        dcf_display,
        hide_index=True,
        use_container_width=True
    )

with col2:
    st.markdown('<div class="section-title">Free Cash Flow Projection</div>', unsafe_allow_html=True)
    
    # FCFF data (from Free Cash Flow sheet)
    fcff = [506.73, 1083.25, -2798.56, 765.68, 701.92, 3900.56, 1950.87, 4737.71, 7360.97, 10695.53, 13040.62]
    
    # Create chart
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        x=years, 
        y=fcff, 
        name='FCFF', 
        marker_color=['#e74c3c' if y < 0 else '#27ae60' for y in fcff]
    ))
    
    fig3.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=30, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis_title="₹ Crores",
        showlegend=False
    )
    
    st.plotly_chart(fig3, use_container_width=True)

# Sensitivity Analysis (from DCF sheet)
st.markdown('<div class="section-title">Share Price Sensitivity Table</div>', unsafe_allow_html=True)

# Sensitivity data (directly from DCF sheet)
sensitivity_data = {
    'Growth Rate': ['4.0%', '4.5%', '5.0%', '5.5%', '6.0%'],
    '7.5% WACC': [2881.37, 3405.42, 4139.10, 5239.61, 7073.79],
    '8.0% WACC': [2440.08, 2825.89, 3340.31, 4060.49, 5140.76],
    '8.5% WACC': [2098.34, 2392.93, 2771.67, 3276.67, 3983.67],
    '9.0% WACC': [1826.25, 2057.62, 2346.83, 2718.68, 3214.48],
    '9.5% WACC': [1604.77, 1790.64, 2017.81, 2301.78, 2666.88]
}

sensitivity_df = pd.DataFrame(sensitivity_data)

# Format for display
def format_price(x):
    return f'₹{x:.0f}'

styled_df = sensitivity_df.style.format({
    '7.5% WACC': format_price,
    '8.0% WACC': format_price,
    '8.5% WACC': format_price,
    '9.0% WACC': format_price,
    '9.5% WACC': format_price
})

st.dataframe(
    styled_df,
    hide_index=True,
    use_container_width=True
)

st.caption("Sensitivity analysis shows intrinsic share price under different WACC and terminal growth assumptions")

# Financial Ratios (from Ratios sheet)
st.markdown('<div class="section-title">Key Financial Ratios</div>', unsafe_allow_html=True)

# Ratios data (directly from Ratios sheet)
ratios_data = {
    'Ratio': ['Current Ratio', 'Quick Ratio', 'Debt to Equity', 'Interest Coverage', 'ROCE', 'Asset Turnover'],
    '2020': [0.7, 0.16, 0.53, 14.8, 0.24, 4.19],
    '2025': [0.32, 0.22, 1.12, 6.0, 0.23, 5.03],
    '2030': [0.29, 0.12, 0.13, 18.99, 0.25, 6.07]
}

ratios_df = pd.DataFrame(ratios_data)

# Format for display
def format_ratio(x):
    if isinstance(x, str):
        return x
    if x > 1:
        return f'{x:.1f}x'
    return f'{x:.2f}x'

# Apply formatting
ratios_df['2020'] = ratios_df['2020'].apply(format_ratio)
ratios_df['2025'] = ratios_df['2025'].apply(format_ratio)
ratios_df['2030'] = ratios_df['2030'].apply(format_ratio)

st.dataframe(
    ratios_df,
    hide_index=True,
    use_container_width=True
)

# Footer
st.divider()
st.caption("Note: This valuation is based on historical data from FY2020-FY2025 and projections through FY2030. All figures in Indian Rupees Crores.")