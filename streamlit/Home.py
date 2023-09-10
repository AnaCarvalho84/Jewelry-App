#Libraries
import streamlit as st  
import warnings
warnings.filterwarnings('ignore')
from st_pages import Page, add_page_title, show_pages

#Page Configuration
st.set_page_config(page_title='Jewelry Store Data Analysis', page_icon=':gem:', layout='wide', initial_sidebar_state='expanded')

# CSS for text justification
st.markdown("""
<style>
    .reportview-container .markdown-text-container {
        text-align: justify;
    }
</style>
""", unsafe_allow_html=True)

# List of pages with their titles and icons
pages = [
    Page("Home.py", "Home", "🏠"),
    Page("pages\Store_Analysis.py", "Store Analysis", "🛍️"),
    Page("pages\Product Analysis.py", "Product Analysis", "📦"),
    Page("pages\Profile Consumer.py", "Profile Consumer", "👤"),
    Page("pages\Analysis of External Factors.py", "Analysis of External Factors", "🌍"),
    Page("pages\Social Media.py", "Social Media", "📱"),
]

# Get the current page's URL
current_page = st.experimental_get_query_params().get("page", None)

# Display the pages in the sidebar
show_pages(pages)


#Box for Upload CSV file
uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])
if uploaded_file:
    st.sidebar.write("File uploaded successfully!")

st.title(":gem: Jewelry Store Data Analysis")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)
st.markdown(" ")
st.markdown("---")

# Display the icons side by side with their titles
col1, col2 = st.columns(2)
# Store 1 Icon and Title
with col1:
    icon_col1, text_col1 = st.columns([1, 4])  
    with icon_col1:
        st.image(r"images\store1.png", width=50)
    with text_col1:
        st.subheader("**_Jewelry Store 1_**")
    st.markdown("Located in an area with <b><u>19,576</u></b> inhabitants. <br> Open since 1986 - in the historic center of the city", unsafe_allow_html=True)

# Store 2 Icon and Title
with col2:
    icon_col2, text_col2 = st.columns([1, 4])  
    with icon_col2:
        st.image(r"images\store2.png", width=50)
    with text_col2:
        st.subheader("**_Jewelry Store 2_**")
    st.markdown("Located in an area with <b><u>7,193</u></b> inhabitants. <br> Open since 2011 - in the residential center of the city", unsafe_allow_html=True)
st.markdown("---")
st.subheader('Strategic Analysis')

# Justifying the main text using direct HTML
st.markdown("""
<div style="text-align: justify">
    <p style="text-indent: 1em;">This project aims to analyze the data from two jewelry stores and extract analytical insights in order to improve the performance of both stores and, in the future, expand the business to a third store.</p>
    <p style="text-indent: 1em;">The data was collected from a real database of a jewelry business.</p>
    <p style="text-indent: 1em;">The data spans from <strong><em><u>January 2018 to August 2023.</u></em></strong></p>
</div>
""", unsafe_allow_html=True)
st.markdown(" ")
st.markdown(" ")
st.subheader('Methodology')
st.markdown("""
<div style="text-align: justify">
   <p style="text-indent: 1em;">The methodology used involved requesting the databases from the responsible person for both stores, conducting an analysis of the databases, performing data cleaning and processing, and conducting an exploratory data analysis, making comparisons between both stores. Sales and profits were analyzed, and efforts were made to understand which products are the best-selling, as well as the material composition of each product. Techniques such as cross-selling were applied.

<p style="text-indent: 1em;">The impact of weather conditions was evaluated since both stores are located in a local commercial area. Regarding consumers, the impact of salary receipt on the sales of both stores was studied, and a t-test was applied to test the suggested hypotheses. Differences between genders in purchases and the average amount spent by each gender are presented. A statistical test was also conducted to understand if there are differences between sales to men and women for each of the stores.


</div>
""", unsafe_allow_html=True)

st.subheader('Future Works')
st.markdown("""
<div style="text-align: justify">
   One of the prime avenues for evolution is data integration. By moving beyond traditional CSV or Excel uploads and embracing real-time databases and diverse data sources, we can paint a richer, more dynamic picture of business landscapes. This integration would seamlessly complement user empowerment. By granting users the capability to personalize their visualizations, from chart types to specific date ranges, we not only cater to their preferences but also make their analytical journey more intuitive.

Feedback is the compass that can guide our developmental trajectory. A dedicated mechanism to capture user insights can be the lighthouse, shedding light on areas of improvement and new features. As we reflect on the past and present, there's also merit in anticipating the future. Through predictive analysis rooted in historical data, we can chart out potential future sales or product performance trends, offering businesses a strategic advantage.

User trust is the cornerstone of our platform. By fortifying our defenses with enhanced authentication measures, we ensure that our sanctum of data remains inviolable. And while we safeguard the present, real-time notifications can keep users abreast of significant business shifts, from sales fluctuations to product performance metrics.

As our data universe expands, efficiency becomes paramount. Adopting cutting-edge optimization techniques will ensure our platform remains nimble, delivering insights without delay. Finally, in our interconnected digital era, forging alliances with other platforms, be it CRM systems or e-commerce portals, can amplify our analytical prowess. Such integrations offer a panoramic view of businesses, making decision-making more informed and strategic.

In essence, these evolutions aren't just enhancements; they're the stepping stones to establishing our application as a gold standard in data analytics.
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
   st.info('**Data Analyst: [@AnaCarvalho84](mailto:ac@anadecarvalho.pt)**', icon="📧")
with c2:
    st.info('**GitHub: [@AnaCarvalho](https://github.com/AnaCarvalho84)**', icon="💻")
with c3:
    st.info('**Linkedin: [AnaCarvalho](https://www.linkedin.com/in/anafpcarvalho84/)**', icon="🧠")