import streamlit as st
from pages import (
    show_login_page,
    show_register_page,
    show_user_info,
    show_job_description_test,
    show_upload_cv,
    show_explore_data,
    show_visualize_data,
)
from utils import get_query_params, set_query_params
from auth import perform_logout

# Initialize session state
if "token" not in st.session_state:
    st.session_state["token"] = None

# Check if the token is stored in session state or URL parameters
query_params = get_query_params()
if st.session_state["token"] is None and "token" in query_params:
    st.session_state["token"] = query_params["token"][0]
    st.markdown(
        f"<script>window.history.replaceState(null, null, window.location.pathname);</script>",
        unsafe_allow_html=True,
    )


# Function to display the application name
def show_app_name():
    st.markdown(
        """
        <style>
        .app-name {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #4CAF50;  /* Change color as needed */
            margin-bottom: 20px;
        }
        </style>
        <div class="app-name">SmartRecruit</div>
        """,
        unsafe_allow_html=True,
    )


# Main logic
show_app_name()
if st.session_state["token"]:
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select a page",
        [
            "User Info",
            "Resume Ranker",
            "Upload CV",
            "Explore Stored Data",
            "Data Visualization ",
        ],
    )

    if page == "User Info":
        show_user_info()
    elif page == "Resume Ranker":
        show_job_description_test()
    elif page == "Upload CV":
        show_upload_cv()
    elif page == "Explore Stored Data":
        show_explore_data()
    elif page == "Data Visualization ":
        show_visualize_data()

    if st.sidebar.button("Logout"):
        perform_logout()
else:
    st.title("User Authentication")
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select a page", ["Login", "Register"])

    if page == "Login":
        show_login_page()
    else:
        show_register_page()
