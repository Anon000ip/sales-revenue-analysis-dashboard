import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales & Revenue Analysis Dashboard", layout="wide")

@st.cache_data
def load_data():
    data = {
        'Date': ['2026-09-01', '2026-09-05', '2026-09-12', '2026-09-18', '2026-09-25'],
        'Product': ['Laptop Pro', 'Wireless Mouse', 'Monitor 27in', 'Mechanical Keyboard', 'Laptop Pro'],
        'Category': ['Electronics', 'Accessories', 'Electronics', 'Accessories', 'Electronics'],
        'Region': ['North', 'South', 'East', 'West', 'South'],
        'Quantity': [15, 40, 22, 30, 10],
        'Revenue': [18000, 1200, 6600, 2400, 12000]
    }
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

st.title("📊 Sales & Revenue Analysis Dashboard")

st.sidebar.header("Filter Options")
selected_region = st.sidebar.multiselect("Select Region", options=df['Region'].unique(), default=df['Region'].unique())
selected_category = st.sidebar.multiselect("Select Category", options=df['Category'].unique(), default=df['Category'].unique())

filtered_df = df[(df['Region'].isin(selected_region)) & (df['Category'].isin(selected_category))]

total_revenue = filtered_df['Revenue'].sum()
total_units = filtered_df['Quantity'].sum()

col1, col2 = st.columns(2)
col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Total Units Sold", f"{total_units}")

st.subheader("Revenue Trends Over Time")
if not filtered_df.empty:
    trend_data = filtered_df.groupby('Date')['Revenue'].sum().reset_index()
    fig_trend = px.line(trend_data, x='Date', y='Revenue', markers=True, title="Daily Revenue Trend")
    st.plotly_chart(fig_trend, use_container_width=True)

    st.subheader("Top-Performing Products by Revenue")
    prod_data = filtered_df.groupby('Product')['Revenue'].sum().reset_index().sort_values(by='Revenue', ascending=False)
    fig_prod = px.bar(prod_data, x='Revenue', y='Product', orientation='h', title="Revenue by Product")
    st.plotly_chart(fig_prod, use_container_width=True)
else:
    st.warning("No data found for the selected filters.")
