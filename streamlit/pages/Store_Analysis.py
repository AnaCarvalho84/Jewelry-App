# Libraries
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os
import warnings
import plotly.graph_objects as go
warnings.filterwarnings('ignore')
import pickle
from mlxtend.frequent_patterns import association_rules

## Page Configuration
st.set_page_config(page_title='Stores Analysis', page_icon=':chart_with_upwards_trend:', layout='wide', initial_sidebar_state='expanded')
st.title(":chart_with_upwards_trend: Stores Analysis")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

## Load the data
df = pd.read_csv("Sales.csv", encoding="ISO-8859-1")

## Convert the 'DATE' column to datetime type
df['DATE'] = pd.to_datetime(df['DATE'])

## Filters 
col1, col2,col3 = st.columns(3)

# Date Range Filter in the first column
with col1:
    start_date, end_date = st.date_input("Select Date Range", [df['DATE'].min(), df['DATE'].max()], key='date_range_selector')

# Convert the Python date objects to pandas Timestamps for comparison
start_date = pd.Timestamp(start_date)
end_date = pd.Timestamp(end_date)
filtered_data = df[(df['DATE'] >= start_date) & (df['DATE'] <= end_date)]

# Store_ID Filter in the second column
with col2:
    unique_stores = sorted(df['Store_ID'].unique())
    selected_stores = st.multiselect('Select Store(s)', unique_stores, default=unique_stores)
    filtered_data = filtered_data[filtered_data['Store_ID'].isin(selected_stores)]

# Seller Filter in the third column
with col3:
    unique_sellers = sorted(df['SELLER'].unique())
    selected_sellers = st.multiselect('Select Seller(s)', unique_sellers, default=unique_sellers)
    filtered_data = filtered_data[filtered_data['SELLER'].isin(selected_sellers)]


##Sales
st.header("Sales")
# Group by both DATE and Store_ID and sum TOTAL_SALES
grouped_data = filtered_data.groupby([filtered_data['DATE'].dt.to_period("Q"), 'Store_ID'])[['TOTAL_SALES']].sum().reset_index()
store1_sales = grouped_data[grouped_data['Store_ID'] == 1]['TOTAL_SALES'].sum()
store2_sales = grouped_data[grouped_data['Store_ID'] == 2]['TOTAL_SALES'].sum()

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.markdown("<h2 style='font-size:25px;'>💰 Both Stores</h2>", unsafe_allow_html=True)
    st.subheader(f"{grouped_data['TOTAL_SALES'].sum():,.2f} €")

with middle_column:
    st.markdown("<h2 style='font-size:25px;'>🥇 Store 1</h2>", unsafe_allow_html=True)
    st.subheader(f"{store1_sales:,.2f} €")

with right_column:
    st.markdown("<h2 style='font-size:25px;'>🥈 Store 2</h2>", unsafe_allow_html=True)
    st.subheader(f"{store2_sales:,.2f} €")

st.markdown("---")



##Total Sales for Both Stores
# Group data by quarter
grouped_data = filtered_data.groupby([filtered_data['DATE'].dt.to_period("Q"), 'Store_ID'])[['TOTAL_SALES']].sum().reset_index()
    
# Convert 'DATE' column to a format that shows both the year and the quarter
grouped_data['DATE'] = grouped_data['DATE'].astype(str)
    
# Create a pivot table for plotting
pivot_data = grouped_data.pivot(index='DATE', columns='Store_ID', values='TOTAL_SALES')

# Create the plot
fig = px.line(pivot_data, x=pivot_data.index, y=pivot_data.columns, 
                  title='Total Sales by Trimester', labels={'value': 'Total Sales', 'variable': 'Store_ID'})
    
# Rotate the x-axis labels by 45 degrees
fig.update_xaxes(tickangle=45)

# Adjust the width of the plot
fig.update_layout(width=900)  

st.plotly_chart(fig, theme="streamlit")

st.markdown("---")


##PROFIT&Sales
# Colors for Sales and Profit for both stores
colors = {
    (1, 'Sales'): 'darkblue',
    (1, 'Profit'): 'darkblue',
    (2, 'Sales'): 'lightblue',
    (2, 'Profit'): 'lightblue'}

fig = go.Figure()

# Assuming the DATE column in filtered_data is a datetime type
filtered_data['YEAR'] = filtered_data['DATE'].dt.year

# Aggregate yearly sales and profit for each store
sales_profit_analysis_yearly = filtered_data.groupby(['Store_ID', 'YEAR']).agg({'TOTAL_SALES': 'sum', 'PROFIT': 'sum'}).reset_index()

# Plotting Sales
for store_id in [1, 2]:
        subset = sales_profit_analysis_yearly[sales_profit_analysis_yearly['Store_ID'] == store_id]
        fig.add_trace(go.Scatter(x=subset['YEAR'], y=subset['TOTAL_SALES'], mode='lines', 
                                 name=f'Sales - Store {store_id}', line=dict(color=colors[(store_id, 'Sales')], dash='solid')))

# Plotting Profit
for store_id in [1, 2]:
        subset = sales_profit_analysis_yearly[sales_profit_analysis_yearly['Store_ID'] == store_id]
        fig.add_trace(go.Scatter(x=subset['YEAR'], y=subset['PROFIT'], mode='lines', 
                                 name=f'Profit - Store {store_id}', line=dict(color=colors[(store_id, 'Profit')], dash='dash')))

fig.update_layout(title='Total Sales and Profit Over the Years for Both Stores',
                      xaxis_title='Year',
                      yaxis_title='Amount',
                      legend_title='Legend',
                      template='plotly_white',
                      width=900) 
st.plotly_chart(fig, theme="streamlit")


