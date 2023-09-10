#Libraries
import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go

## Page Configuration
st.set_page_config(page_title="Analysis External Factors", page_icon=":chart_with_upwards_trend:", layout="wide")
st.title('Environmental Factors ☀️ ☁️ 🌧️')

## Load the data 
df = pd.read_csv("Sales.csv", encoding="ISO-8859-1")

# Convert the 'DATE' column to datetime type
df['DATE'] = pd.to_datetime(df['DATE'])

# Create columns for the plots
col_plot1, col_plot2 = st.columns(2)

## Sales vs. Temperature
with col_plot1:
    fig1 = px.scatter(df, x='TEMPERATURE', y='TOTAL_SALES', title="Sales vs. Temperature")
    st.plotly_chart(fig1)

## Sales vs. Precipitation
with col_plot2:
    fig2 = px.scatter(df, x='PRECIPITATION', y='TOTAL_SALES', title="Sales vs. Precipitation")
    st.plotly_chart(fig2)

## Sales vs. Cloud Cover
fig3 = px.scatter(df, x='CLOUDCOVER(%)', y='TOTAL_SALES', title="Sales vs. Cloud Cover")
st.plotly_chart(fig3)

st.markdown("""
Based on the calculated correlations, it appears that meteorological factors do not have a strong linear relationship with sales. From what we observed in the plots, these factors do not seem to have a direct linear impact on sales in this dataset.
""")

### Salary 
st.title('Impact of Salary on Sales 💵')
# Extracting day of the month from the DATE column
df['DAY_OF_MONTH'] = df['DATE'].dt.day

# Calculating average sales for each day of the month and store
average_sales_by_day = df.groupby(['DAY_OF_MONTH', 'Store_ID'])['TOTAL_SALES'].mean().reset_index()

# Filter data for each store
store1_data = average_sales_by_day[average_sales_by_day['Store_ID'] == 1]
store2_data = average_sales_by_day[average_sales_by_day['Store_ID'] == 2]

# Create a line plot using plotly
fig = go.Figure()


fig.add_trace(go.Scatter(x=store1_data['DAY_OF_MONTH'], 
                         y=store1_data['TOTAL_SALES'],
                         mode='lines+markers',
                         name='Store 1',
                         line=dict(color='darkblue')))


fig.add_trace(go.Scatter(x=store2_data['DAY_OF_MONTH'], 
                         y=store2_data['TOTAL_SALES'],
                         mode='lines+markers',
                         name='Store 2',
                         line=dict(color='lightblue')))

# Highlight the expected payday period
fig.add_vrect(x0="20.5", x1="31.5", 
              fillcolor="yellow", opacity=0.2,
              layer="below", line_width=0, 
              annotation_text="Expected Payday Period (21-31)")

# Update layout properties
fig.update_layout(title='Impact of the Customers Salary Receipt on Sales',
                  xaxis_title='Day of Month',
                  yaxis_title='Average Sales',
                  xaxis=dict(tickvals=list(range(1, 32))),
                  showlegend=True)


st.plotly_chart(fig)


# Custom CSS for justified text and line spacing
st.markdown("""
    <style>
        .justified-text {
            text-align: justify;
            line-height: 1.5;
        }
    </style>
""", unsafe_allow_html=True)

# Apply the custom style to the text
st.markdown("""
    <div class="justified-text">
        From a preliminary observation, it seems there might be a slight increase in sales towards the end of the month for Store 1. However, the pattern is not very pronounced for Store 2. After conducting a statistical analysis to compare the average sales between the days of the payment period and the other days, there is a significant difference in average sales between the payday period and other days of the month for Store 1. This suggests that the payday period might have an influence on sales for Store 1. In contrast, this pattern doesn't occur for Store 2, and the payday period doesn't seem to influence its sales.
    </div>
""", unsafe_allow_html=True)
