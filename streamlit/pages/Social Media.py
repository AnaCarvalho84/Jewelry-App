#Libraries
import pandas as pd
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt

## Page Configuration
st.set_page_config(page_title="Social Media", page_icon=":chart_with_upwards_trend:", layout="wide")
st.title('📱 Social Media')

# Load the social media data
social = pd.read_excel("SocialMedias.xlsx")

# Calculate the average rating
average_rating = social['rating'].mean()

# Display the average rating using Markdown right after the title
st.markdown(f"⭐⭐⭐⭐⭐ **Average Rating:** {average_rating:.2f}")

def main():
    # Generating the word cloud
    comments = pd.read_pickle("comments.pkl")
    wordcloud = WordCloud(background_color='white', width=1000, height=200, max_words=150).generate(" ".join(comments))

    # Display the word cloud
    st.set_option('deprecation.showPyplotGlobalUse', False)  # To avoid a warning
    plt.figure(figsize=(10, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('')
    st.pyplot()

if __name__ == "__main__":
    main()
    
st.markdown(" ")
st.write(social)
