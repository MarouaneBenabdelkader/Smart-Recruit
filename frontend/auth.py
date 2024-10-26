import requests
import streamlit as st

backend_url = "http://localhost:8000"  # Replace with your actual backend URL


def authenticate_user(email, password):
    response = requests.post(
        f"{backend_url}/token", data={"username": email, "password": password}
    )
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        st.error("Login failed! Please check your credentials and try again.")
        return None


def register_user(full_name, email, password, department, company_name):
    response = requests.post(
        f"{backend_url}/register",
        json={
            "full_name": full_name,
            "email": email,
            "password": password,
            "department": department,
            "company_name": company_name,
        },
    )
    if response.status_code == 200:
        st.success("Registration successful! Please log in.")
    else:
        st.error(
            f"Registration failed: {response.json().get('detail', 'Unknown error')}"
        )


def get_user_data(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{backend_url}/users/me/", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error: {response.status_code}")
        return None


def perform_logout():
    st.session_state["token"] = None
    st.markdown(
        f"<script>window.history.replaceState(null, null, window.location.pathname);</script>",
        unsafe_allow_html=True,
    )
    st.rerun()
