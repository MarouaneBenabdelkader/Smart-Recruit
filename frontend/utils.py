import streamlit as st


def set_query_params(**params):
    query_str = "&".join(
        [f"{key}={value}" for key, value in params.items() if value is not None]
    )
    st.markdown(
        f"<script>window.history.replaceState(null, null, window.location.pathname + '?{query_str}');</script>",
        unsafe_allow_html=True,
    )


def get_query_params():
    return st.query_params
