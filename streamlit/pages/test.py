import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page

def homepage():
    st.title("Home Page")
    # Add content for the home page here

def upload_page():
    st.title("Upload Page")
    # Add content for the upload page here

def analytics_page():
    st.title("Analytics Page")
    # Add content for the analytics page here

def contact_page():
    st.title("Contact Page")
    # Add content for the contact page here

def main():
    selected = option_menu(
        menu_title=None,
        options=["Home", "Upload", "Analytics", 'Settings', 'Contact'],
        icons=[':house:', ':cloud-upload:', ":graph-up-arrow:", ':gear:', ':phone:'],
        menu_icon="cast",
        orientation="horizontal",
        styles={
            "nav-link": {
                "text-align": "left",
                "--hover-color": "#A52A2A",
            }
        }
    )

    if selected == "Home":
        homepage("Home.py")
    elif selected == "Upload":
        upload_page()
    elif selected == "Analytics":
        analytics_page("pages\1_Store_Analysis.py")
    elif selected == "Contact":
        contact_page()

if __name__ == "__main__":
    main()
