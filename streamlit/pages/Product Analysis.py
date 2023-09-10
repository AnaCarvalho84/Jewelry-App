# Libraries
import pandas as pd
import streamlit as st
import warnings
import plotly.graph_objects as go
warnings.filterwarnings('ignore')

## Page Configuration
st.set_page_config(page_title='Product Analysis', page_icon=':gem:', layout='wide', initial_sidebar_state='expanded')
st.title(":bar_chart: Product Analysis")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

## Load the data 
df = pd.read_csv("Sales.csv", encoding="ISO-8859-1")

# Convert the 'DATE' column to datetime type
df['DATE'] = pd.to_datetime(df['DATE'])

## Create columns for the filters
col1, col2, col3, col4 = st.columns(4)

# Date Range Filter in the first column
with col1:
    start_date, end_date = st.date_input("Select Date Range", [df['DATE'].min(), df['DATE'].max()], key='date_range_selector')

# Convert the Python date objects to pandas Timestamps for comparison
start_date = pd.Timestamp(start_date)
end_date = pd.Timestamp(end_date)

filtered_data = df[(df['DATE'] >= start_date) & (df['DATE'] <= end_date)]

##PRODUCT and sum TOTAL_SALES
grouped_product_data = filtered_data.groupby(['PRODUCT'])[['TOTAL_SALES']].sum()['TOTAL_SALES']
most_sold_product = grouped_product_data.idxmax()
most_sold_product_sales = grouped_product_data.max()

# Group by PRODUCT for Store 1 and sum TOTAL_SALES
grouped_product_store1 = filtered_data[filtered_data['Store_ID'] == 1].groupby(['PRODUCT'])['TOTAL_SALES'].sum()
most_sold_product_store1 = grouped_product_store1.idxmax()
most_sold_product_sales_store1 = grouped_product_store1.max()

# Group by PRODUCT for Store 2 and sum TOTAL_SALES
grouped_product_store2 = filtered_data[filtered_data['Store_ID'] == 2].groupby(['PRODUCT'])['TOTAL_SALES'].sum()
most_sold_product_store2 = grouped_product_store2.idxmax()
most_sold_product_sales_store2 = grouped_product_store2.max()

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.markdown("<h2 style='font-size:25px;'>🏆 Most Sold Product</h2>", unsafe_allow_html=True)
    st.write(f"Product: {most_sold_product}")
    st.subheader(f"€ {most_sold_product_sales:,.2f}")

with middle_column:
    st.markdown("<h2 style='font-size:25px;'>🥇 Store 1</h2>", unsafe_allow_html=True)
    st.write(f"Product: {most_sold_product_store1}")
    st.subheader(f"€ {most_sold_product_sales_store1:,.2f}")

with right_column:
    st.markdown("<h2 style='font-size:25px;'>🥈 Store 2</h2>", unsafe_allow_html=True)
    st.write(f"Product: {most_sold_product_store2}")
    st.subheader(f"€ {most_sold_product_sales_store2:,.2f}")
    
st.markdown("---")


# Store_ID Filter in the second column
with col2:
    unique_stores = sorted(df['Store_ID'].unique())
    selected_stores = st.multiselect('Select Store_ID(s)', unique_stores)
    if selected_stores:
        filtered_data = filtered_data[filtered_data['Store_ID'].isin(selected_stores)]

# PRODUCT Filter in the third column
with col3:
    unique_products = sorted(df['PRODUCT'].unique())
    selected_products = st.multiselect('Select PRODUCT(s)', unique_products)
    if selected_products:
        filtered_data = filtered_data[filtered_data['PRODUCT'].isin(selected_products)]

# MATERIAL Filter in the fourth column
with col4:
    unique_materials = sorted(df['MATERIAL'].unique())
    selected_materials = st.multiselect('Select MATERIAL(s)', unique_materials)
    if selected_materials:
        filtered_data = filtered_data[filtered_data['MATERIAL'].isin(selected_materials)]

st.write(filtered_data)


## Top 10 Products Sold by Quantity
top_products_store1 = filtered_data[filtered_data['Store_ID'] == 1]['PRODUCT'].value_counts().nlargest(10)
top_products_store2 = filtered_data[filtered_data['Store_ID'] == 2]['PRODUCT'].value_counts().nlargest(10)

merged_top_products = pd.concat([top_products_store1, top_products_store2], axis=1, keys=['Store 1', 'Store 2'])
merged_top_products = merged_top_products.fillna(0) 

fig = go.Figure()

# Adding data for Store 1 with darkblue color
fig.add_trace(go.Bar(
    x=merged_top_products.index,
    y=merged_top_products['Store 1'],
    name='Store 1',
    marker=dict(color='darkblue')  
))

# Adding data for Store 2 with lightblue color
fig.add_trace(go.Bar(
    x=merged_top_products.index,
    y=merged_top_products['Store 2'],
    name='Store 2',
    marker=dict(color='lightblue')  
))

fig.update_layout(title_text='Top 10 Products by Quantity',
                  xaxis_title="Product",
                  yaxis_title="Quantity",
                  barmode='group',      
                  width=800,
                  height=500)

st.plotly_chart(fig)

##Top 10 Least Products
# List for the least sold itemns
least_sold_figs = []

# Loop through the unique store IDs
for store in filtered_data['Store_ID'].unique():
    
    # Filter the data for the current store
    store_sales = filtered_data[filtered_data['Store_ID'] == store]
    
    # Get the bottom 10 products by sales for the current store
    product_sales_store = store_sales['PRODUCT'].value_counts().nsmallest(10)

    # Create a bar chart using Plotly
    fig = go.Figure(go.Bar(
        y=product_sales_store.index,
        x=product_sales_store.values,
        orientation='h',
        marker=dict(color=product_sales_store.values)
    ))

    fig.update_layout(title_text=f'Least 10 Products by Sales for Store {store}',
                      xaxis_title="Quantity",
                      yaxis_title="Product",
                      yaxis_categoryorder = 'total ascending',
                      width=400,  # Definindo a largura
                      height=500) # Definindo a altura

    least_sold_figs.append(fig)


# Get the bottom 10 products by quantity for Store 1
least_sold_store1 = filtered_data[filtered_data['Store_ID'] == 1]['PRODUCT'].value_counts().nsmallest(10)

# Get the bottom 10 products by quantity for Store 2
least_sold_store2 = filtered_data[filtered_data['Store_ID'] == 2]['PRODUCT'].value_counts().nsmallest(10)

# Merge the two series into a single dataframe
merged_least_sold = pd.concat([least_sold_store1, least_sold_store2], axis=1, keys=['Store 1', 'Store 2'])
merged_least_sold = merged_least_sold.fillna(0)  # Fill NaN values with 0

# Sort the merged dataframe by total sales across both stores
merged_least_sold['Total'] = merged_least_sold['Store 1'] + merged_least_sold['Store 2']
merged_least_sold = merged_least_sold.sort_values(by='Total')

# Create a bar chart using Plotly
fig = go.Figure()

# Add data for Store 1
fig.add_trace(go.Bar(
    x=merged_least_sold.index,
    y=merged_least_sold['Store 1'],
    name='Store 1',
    marker=dict(color='darkblue')
))

# Add data for Store 2
fig.add_trace(go.Bar(
    x=merged_least_sold.index,
    y=merged_least_sold['Store 2'],
    name='Store 2',
    marker=dict(color='lightblue')
))

fig.update_layout(title_text='Least 10 Products by Quantity',
                  xaxis_title="Product",
                  yaxis_title="Quantity",
                  barmode='group',  # Grouped bar chart mode
                  width=800,
                  height=500)

st.plotly_chart(fig)

##Plot Material
# Aggregate the total sales for each material for Store 1
material_sales_store1 = df[df['Store_ID'] == 1].groupby('MATERIAL')['TOTAL_SALES'].sum().nlargest(10)
material_sales_store2 = df[df['Store_ID'] == 2].groupby('MATERIAL')['TOTAL_SALES'].sum().nlargest(10)
merged_material_sales = pd.concat([material_sales_store1, material_sales_store2], axis=1, keys=['Store 1', 'Store 2']).fillna(0)
sales_fig = go.Figure()
sales_fig.add_trace(go.Bar(x=merged_material_sales.index, y=merged_material_sales['Store 1'], name='Store 1', marker=dict(color='darkblue')))
sales_fig.add_trace(go.Bar(x=merged_material_sales.index, y=merged_material_sales['Store 2'], name='Store 2', marker=dict(color='lightblue')))
sales_fig.update_layout(title_text='Top 10 Materials by Sales for Both Stores', xaxis_title="Material", yaxis_title="Total Sales", barmode='group', width=800, height=500)

# Aggregate the total quantity for each material for Store 1
material_quantity_store1 = df[df['Store_ID'] == 1].groupby('MATERIAL')['QTD'].sum().nlargest(10)
material_quantity_store2 = df[df['Store_ID'] == 2].groupby('MATERIAL')['QTD'].sum().nlargest(10)
merged_material_quantity = pd.concat([material_quantity_store1, material_quantity_store2], axis=1, keys=['Store 1', 'Store 2']).fillna(0)
quantity_fig = go.Figure()
quantity_fig.add_trace(go.Bar(x=merged_material_quantity.index, y=merged_material_quantity['Store 1'], name='Store 1', marker=dict(color='darkblue')))
quantity_fig.add_trace(go.Bar(x=merged_material_quantity.index, y=merged_material_quantity['Store 2'], name='Store 2', marker=dict(color='lightblue')))
quantity_fig.update_layout(title_text='Top 10 Materials by Quantity for Both Stores', xaxis_title="Material", yaxis_title="Total Quantity", barmode='group', width=800, height=500)

# Display the charts side by side in Streamlit
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(sales_fig)
with col2:
    st.plotly_chart(quantity_fig)



###Evolution of the products 
# Convert the 'DATE' column to datetime type
df['DATE'] = pd.to_datetime(df['DATE'])

# Extract the year from the 'DATE' column
df['YEAR'] = df['DATE'].dt.year

# Filter widget setup
# Create columns for the filters
col1, col2, col3 = st.columns(3)

# Year Filter in the first column
with col1:
    unique_years = sorted(df['YEAR'].unique())
    selected_years = st.multiselect('Select YEAR(s)', ['All'] + unique_years, default='All', key="year_select")

# Store_ID Filter in the second column
with col2:
    unique_stores = sorted(df['Store_ID'].unique())
    selected_stores = st.multiselect('Select Store_ID(s)', unique_stores, key="store_select_1")

# PRODUCT Filter in the third column
with col3:
    unique_products = sorted(df['PRODUCT'].unique())
    selected_products = st.multiselect('Select PRODUCT(s)', unique_products, key="product_select")

# Check if 'All' is selected in the year filter
if 'All' in selected_years:
    selected_years = unique_years

# Apply the filters
if selected_years:
    df = df[df['YEAR'].isin(selected_years)]
if selected_stores:
    df = df[df['Store_ID'].isin(selected_stores)]
if selected_products:
    df = df[df['PRODUCT'].isin(selected_products)]

# Group by both YEAR and PRODUCT and sum TOTAL_SALES
product_sales_evolution = df.groupby(['YEAR', 'Store_ID', 'PRODUCT']).agg({'TOTAL_SALES': 'sum'}).reset_index()

# Plotting the data for each product with the given colors
fig = go.Figure()

for product in selected_products:
    for store_id, color in zip([1, 2], ['darkblue', 'lightblue']):
        subset = product_sales_evolution[(product_sales_evolution['PRODUCT'] == product) & (product_sales_evolution['Store_ID'] == store_id)]
        fig.add_trace(go.Scatter(x=subset['YEAR'], y=subset['TOTAL_SALES'], mode='lines+markers', name=f'Store {store_id} - {product}'))

fig.update_layout(title='Product Sales Evolution Over Years', xaxis_title='Year', yaxis_title='Total Sales', xaxis=dict(tickvals=unique_years))
st.plotly_chart(fig)


# Assuming 'df' is the name of your dataframe in the Streamlit script
df = pd.read_csv("Sales.csv", encoding="ISO-8859-1")
df['YEAR'] = pd.to_datetime(df['DATE']).dt.year

# Grouping by Store_ID, YEAR, and PRODUCT to get the total PROFIT for each product per store per year
product_profit = df.groupby(['Store_ID', 'YEAR', 'PRODUCT']).agg({'PROFIT': 'sum'}).reset_index()

# Filtering the product with the highest profit for each Store and YEAR combination
max_profit_product = product_profit.sort_values('PROFIT', ascending=False).drop_duplicates(subset=['Store_ID', 'YEAR'])

def create_final_interactive_chart(data):
    # Create grouped bar chart using Plotly
    fig = go.Figure()
    
    # Define the store colors
    colors = {1: "darkblue", 2: "lightblue"}
    
    # Iterate through each store and plot the data
    for store in [1, 2]:  # Only for Store 1 and Store 2
        store_data = data[data['Store_ID'] == store]
        fig.add_trace(go.Bar(
            x=store_data['YEAR'],
            y=store_data['PROFIT'],
            name=f'Store {store}',
            text=store_data['PRODUCT'],
            textposition='outside',
            marker_color=colors[store]
        ))
    
    # Adjusting the layout
    fig.update_layout(
        title="Most Profitable Product by Store and by Year",
        xaxis_title="Year",
        yaxis_title="Profit",
        barmode='group',
        legend_title="Store"
    )
    
    return fig

# For use in Streamlit
st.plotly_chart(create_final_interactive_chart(max_profit_product))

## Cross Selling Ancillary Products
st.markdown(" ")

# Load the pickle file
try:
    rules = pd.read_pickle('crossproducts.pkl')

    # Formatting the rules DataFrame
    rules['antecedents'] = rules['antecedents'].apply(lambda x: ', '.join(list(x))).str.replace("frozenset\\(\\{", "").str.replace("\\}\\)", "")
    rules['consequents'] = rules['consequents'].apply(lambda x: ', '.join(list(x))).str.replace("frozenset\\(\\{", "").str.replace("\\}\\)", "")

    # Custom CSS for table size
    st.markdown('''
    <style>
    table {
        width: 100%;
        border-collapse: collapse;
        border-spacing: 0;
        border: 1px solid black;
        font-size: 12px;   # Adjusted font size
    }
    th {
        background-color: #f2f2f2;
    }
    th, td {
        text-align: left;
        padding: 8px;
    }
    tr:nth-child(even) {
        background-color: #f2f2f2;
    }
    </style>
    ''', unsafe_allow_html=True)
    
    # Display the icon and title together
    col_icon, col_title = st.columns([1, 6])

    
    with col_title:
        st.markdown("<h2 style='text-align: left; color: black;'>Cross Selling Ancillary Products</h2>", unsafe_allow_html=True)
    st.markdown(" ")
    st.markdown(" ")
    # Splitting Streamlit page into three columns for centering
    col_left_space, col_center, col_right_space = st.columns([1, 6, 1])

    # Displaying the formatted table without the index in the center column
    with col_center:
        st.write(rules[['antecedents', 'consequents', 'lift']].rename(columns={
            'antecedents': 'Item bought 1st (Antecedents)',
            'consequents': 'Item bought after Antecedents (Consequents)',
            'lift': 'Lift'
        }).to_html(index=False), unsafe_allow_html=True)

except FileNotFoundError:
    st.error('The file "crossproducts.pkl" was not found.')
except Exception as e:
    st.error(f"An error occurred: {e}")

#Interpreter Results
st.markdown(" ")
st.markdown("From these results, we can infer:")
st.markdown(" ")
st.markdown("- Customers who purchase a \"CHARM\" are 1.79 times more likely to purchase a \"NECKLACE\" compared to customers who don't purchase a \"CHARM\".")
st.markdown("- Customers who purchase a \"BRACELET WATCH\" are 1.31 times more likely to purchase a \"BATTERY\" compared to customers who don't purchase a \"BRACELET WATCH\".")

