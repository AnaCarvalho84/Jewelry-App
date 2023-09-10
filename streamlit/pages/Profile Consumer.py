#Libraries
import pandas as pd
import streamlit as st
import warnings
import plotly.graph_objects as go
from plotly.subplots import make_subplots

## Page Configuration
st.set_page_config(page_title="Customer Profile", page_icon=":chart_with_upwards_trend:", layout="wide")

## Load the data 
df = pd.read_csv("Sales.csv", encoding="ISO-8859-1")

# Convert the 'DATE' column to datetime type
df['DATE'] = pd.to_datetime(df['DATE'])

st.title('Customer Profile')

# Create side-by-side columns for filters
col_filter1, col_filter2 = st.columns(2)

# Filter for store choice in first column
store_choice = col_filter1.selectbox('Choose a Store', [1, 2])

# Filter for date range in second column
start_date, end_date = col_filter2.date_input("Select Date Range", [df['DATE'].min(), df['DATE'].max()], key='date_range_selector')
start_date = pd.Timestamp(start_date)
end_date = pd.Timestamp(end_date)

# Filter data by gender and store and date range
filtered_data = df[(df['GENDER'].isin(['MALE', 'FEMALE'])) & 
                   (df['Store_ID'] == store_choice) & 
                   (df['DATE'] >= start_date) & 
                   (df['DATE'] <= end_date)]

st.markdown(" ")
# Segment the sales data based on the store choice from the filter
store_data = filtered_data[filtered_data['Store_ID'] == store_choice]

store_1_sales = df[df['Store_ID'] == 1]
store_2_sales = df[df['Store_ID'] == 2]

store_1_gender_data = store_1_sales[store_1_sales['GENDER'].isin(['MALE', 'FEMALE'])]
store_2_gender_data = store_2_sales[store_2_sales['GENDER'].isin(['MALE', 'FEMALE'])]

# Calculating the purchase data
store_1_avg_purchase = store_1_gender_data.groupby('GENDER')['TOTAL_SALES'].mean().round(2).astype(str) + "€"
store_2_avg_purchase = store_2_gender_data.groupby('GENDER')['TOTAL_SALES'].mean().round(2).astype(str) + "€"


# Creating the DataFrame
purchase_gender = pd.DataFrame({
    'Store 1': store_1_avg_purchase,
    'Store 2': store_2_avg_purchase
})

# Adding emojis to the index
purchase_gender = purchase_gender.rename(index={'FEMALE': '👩 FEMALE', 'MALE': '👨 MALE'})

## Create three columns
col1, col2, col3 = st.columns(3)

# Add a title above the table
col1.write("Average amount spent per purchase by Gender")

# Display the dataframe in the middle column
col1.dataframe(purchase_gender)

# Create subplots: 1 row, 2 columns
fig = make_subplots(rows=1, cols=2,
                    subplot_titles=(f'Store {store_choice}: Average Sales by Gender',
                                    f'Store {store_choice}: Distribution of Sales by Gender'))

# Average Sales by Gender
avg_sales = store_data.groupby('GENDER')['TOTAL_SALES'].mean()
fig.add_trace(go.Bar(x=avg_sales.index, y=avg_sales.values, marker_color=['pink', 'lightblue']), row=1, col=1)

# Distribution of Sales by Gender
for gender, color in zip(['MALE', 'FEMALE'], ['lightblue', 'pink']):
    fig.add_trace(go.Box(y=store_data[store_data['GENDER'] == gender]['TOTAL_SALES'], name=gender, marker_color=color), row=1, col=2)

fig.update_layout(showlegend=False)

col2.plotly_chart(fig)