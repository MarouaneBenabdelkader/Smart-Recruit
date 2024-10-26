import requests
import streamlit as st
from auth import authenticate_user, register_user, get_user_data, perform_logout
from utils import set_query_params

from urllib.parse import unquote
from datetime import datetime, time


def show_login_page():
    st.header("Login")
    with st.form(key="login_form"):
        login_email = st.text_input("Login Email")
        login_password = st.text_input("Login Password", type="password")
        login_button = st.form_submit_button("Login")

    if login_button:
        token = authenticate_user(login_email, login_password)
        if token:
            st.session_state["token"] = token
            set_query_params(token=token)
            st.experimental_rerun()


def show_register_page():
    st.header("Register")
    with st.form(key="registration_form"):
        full_name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        department = st.text_input("Department")
        company_name = st.text_input("Company Name")
        register_button = st.form_submit_button("Register")

    if register_button:
        register_user(full_name, email, password, department, company_name)


def show_user_info():
    user_data = get_user_data(st.session_state["token"])
    if user_data:
        full_name = user_data.get("FullName")
        email = user_data.get("Email")
        department = user_data.get("Department")
        company_name = user_data.get("CompanyName")
        resumes = user_data.get("Resumes", [])

        st.header(f"Welcome {full_name} to SmartRecruit")

        st.markdown(
            """
            <style>
            .user-info-table {
                width: 100%;
                border-collapse: collapse;
                box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
                transition: 0.3s;
            }
            .user-info-table:hover {
                box-shadow: 0 8px 16px 0 rgba(0,0,0,0.3);
            }
            .user-info-table, .user-info-table th, .user-info-table td {
                border: 1px solid #e8e8e8;
                padding: 12px 15px;
            }
            .user-info-table th {
                width: 30%;  /* Reduced width for the first column */
                text-align: center;  /* Center aligning text for the headers */
                background-color: #007BFF;
                color: white;
            }
            .user-info-table td {
                text-align: center;  /* Center aligning text for the data cells */
                font-size: 14px;
                color: #333;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <table class="user-info-table">
                <tr>
                    <th>Email</th>
                    <td>{email}</td>
                </tr>
                <tr>
                    <th>Department</th>
                    <td>{department}</td>
                </tr>
                <tr>
                    <th>Company Name</th>
                    <td>{company_name}</td>
                </tr>
                <tr>
                    <th>Number of Resumes</th>
                    <td>{len(resumes)}</td>
                </tr>
            </table>
            """,
            unsafe_allow_html=True,
        )

    else:
        st.session_state["token"] = None
        set_query_params(token=None)
        st.rerun()


# def show_job_description_test():
#     st.header("Job Description Test")
#     st.write(
#         "This section allows you to rank resumes based on a given job description."
#     )

#     token = st.session_state.get("token")
#     if not token:
#         st.error("You need to log in to view this page.")
#         return

#     # Clear button at the top left of the form
#     if st.button("Clear Form"):
#         st.session_state.pop(
#             "job_description", None
#         )  # Removes job description from session state
#         st.session_state.pop(
#             "latest", None
#         )  # Removes latest toggle state from session state
#         st.session_state.pop("size", None)  # Removes size selection from session state
#         st.session_state.pop("ranked_resumes", None)  # Clears any stored ranked resumes
#         st.experimental_rerun()

#     # Form to submit job description and get ranked resumes
#     with st.form(key="job_desc_form"):
#         job_description = st.text_area(
#             "Enter the job description:",
#             value=st.session_state.get("job_description", ""),
#         )
#         latest = st.checkbox(
#             "Include only today's resumes", value=st.session_state.get("latest", False)
#         )
#         size = st.slider(
#             "Number of results to return",
#             min_value=1,
#             max_value=100,
#             value=st.session_state.get("size", 10),
#         )
#         submit_button = st.form_submit_button(label="Rank Resumes")

#     if submit_button:
#         st.session_state["job_description"] = job_description
#         st.session_state["latest"] = latest
#         st.session_state["size"] = size

#         headers = {"Authorization": f"Bearer {token}"}
#         data = {"job_description": job_description, "latest": latest, "size": size}
#         response = requests.get(
#             "http://localhost:8000/rank-resumes", params=data, headers=headers
#         )
#         if response.status_code == 200:
#             st.session_state["ranked_resumes"] = response.json()
#         else:
#             st.error("Failed to fetch ranked resumes. Please try again.")

#     if "ranked_resumes" in st.session_state and st.session_state["ranked_resumes"]:
#         ranked_resumes = st.session_state["ranked_resumes"]
#         st.write("Ranked Resumes:")
#         for idx, resume in enumerate(ranked_resumes, start=1):
#             st.write(
#                 f"{idx}. Resume ID: {resume['resume_id']}, Path: {resume['path']}, Score: {resume['score']}"
#             )
#     elif "ranked_resumes" in st.session_state:
#         st.write("No resumes matched the job description.")


#! stable good working
# def show_job_description_test():
#     st.header("Job Description Test")
#     st.write(
#         "This section allows you to rank resumes based on a given job description."
#     )

#     token = st.session_state.get("token")
#     if not token:
#         st.error("You need to log in to view this page.")
#         return

#     # Clear button at the top left of the form
#     if st.button("Clear Form"):
#         st.session_state.pop(
#             "job_description", None
#         )  # Removes job description from session state
#         st.session_state.pop(
#             "latest", None
#         )  # Removes latest toggle state from session state
#         st.session_state.pop("size", None)  # Removes size selection from session state
#         st.session_state.pop("ranked_resumes", None)  # Clears any stored ranked resumes
#         st.rerun()
#     # style clear button
#     st.markdown(
#         """
#         <style>
#         .stButton>button {
#             background-color: #dc3545;
#             color: white;
#             border-color: #dc3545;
#         }
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )
#     # Form to submit job description and get ranked resumes
#     with st.form(key="job_desc_form"):
#         job_description = st.text_area(
#             "Enter the job description:",
#             value=st.session_state.get("job_description", ""),
#         )
#         latest = st.checkbox(
#             "Include only today's resumes", value=st.session_state.get("latest", False)
#         )
#         size = st.slider(
#             "Number of results to return",
#             min_value=1,
#             max_value=100,
#             value=st.session_state.get("size", 10),
#         )
#         submit_button = st.form_submit_button(label="Rank Resumes")

#     if submit_button:
#         st.session_state["job_description"] = job_description
#         st.session_state["latest"] = latest
#         st.session_state["size"] = size

#         headers = {"Authorization": f"Bearer {token}"}
#         data = {"job_description": job_description, "latest": latest, "size": size}
#         response = requests.get(
#             "http://localhost:8000/rank-resumes", params=data, headers=headers
#         )
#         if response.status_code == 401:
#             st.error("Session expired. Please log in again.")
#             perform_logout()
#             return
#         if response.status_code == 200:
#             st.session_state["ranked_resumes"] = response.json()
#         else:
#             st.error("Failed to fetch ranked resumes. Please try again.")
#     # use fetch_resumes function to get the resumes
#     if "ranked_resumes" in st.session_state and st.session_state["ranked_resumes"]:
#         ranked_resumes = st.session_state["ranked_resumes"]
#         st.write("Ranked Resumes:")
#         for idx, resume in enumerate(ranked_resumes, start=1):
#             st.write(
#                 f"{idx}. Resume ID: {resume['resume_id']}, Path: {resume['path']}, Score: {resume['score']}"
#             )
#     elif "ranked_resumes" in st.session_state:
#         st.write("No resumes matched the job description.")


# * test


def show_job_description_test():
    st.header("Resume Ranker")
    st.write(
        "This section allows you to rank resumes based on a given job description."
    )

    token = st.session_state.get("token")
    if not token:
        st.error("You need to log in to view this page.")
        return

    # Style for the clear button
    st.markdown(
        """
        <style>
        .stButton>button {
            background-color: #dc3545;
            color: white;
            border-color: #dc3545;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Clear Form"):
        # Clearing all relevant session states
        for key in ["job_description", "latest", "size", "ranked_resumes"]:
            st.session_state[key] = None

    with st.form(key="job_desc_form"):
        job_description = st.text_area(
            "Enter the job description:",
            value=st.session_state.get("job_description", ""),
        )
        latest = st.checkbox(
            "Include only today's resumes", value=st.session_state.get("latest", False)
        )
        size = st.slider(
            "Number of results to return",
            min_value=1,
            max_value=100,
            value=st.session_state.get("size", 10),
        )
        submit_button = st.form_submit_button(label="Rank Resumes")

    if submit_button:
        st.session_state.update(
            {"job_description": job_description, "latest": latest, "size": size}
        )
        headers = {"Authorization": f"Bearer {token}"}
        data = {"job_description": job_description, "latest": latest, "size": size}
        response = requests.get(
            "http://localhost:8000/rank-resumes", params=data, headers=headers
        )
        if response.status_code == 401:
            st.error("Session expired. Please log in again.")
            perform_logout()
            return
        if response.status_code == 200:
            st.session_state["ranked_resumes"] = response.json()
        else:
            st.error("Failed to fetch ranked resumes. Please try again.")

    if st.session_state.get("ranked_resumes"):
        headers = {"Authorization": f"Bearer {token}"}
        resumes = fetch_resumes(headers)
        if resumes:
            for resume in resumes:
                ranked_resume = next(
                    (
                        item
                        for item in st.session_state["ranked_resumes"]
                        if item["resume_id"] == resume["resume_id"]
                    ),
                    None,
                )
                if ranked_resume:
                    resume["score"] = ranked_resume.get("score")
            # Filter out resumes that were not ranked (i.e., missing scores)
            resumes = [resume for resume in resumes if "score" in resume]
            resumes.sort(key=lambda x: x["score"], reverse=True)
            display_resumes(resumes)
        else:
            st.error("No resumes found or error in fetching resumes.")
    else:
        st.write("Submit a job description to see rankings.")


def display_resumes(resumes):
    """Display the fetched and scored resumes in the UI"""
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    for idx, resume in enumerate(resumes, start=1):
        with st.expander(
            f"Resume {resume.get('file_path', 'Not available').split('/')[-1]} - Score: {resume['score']} - Uploaded on: {datetime.fromisoformat(resume['upload_date'].replace('Z', '')).strftime('%d %b %Y %H:%M')}"
        ):
            st.markdown(f"**Category:** {resume['category']}")
            st.markdown(f"**Email:** {resume.get('email', 'Not available')}")
            st.markdown(
                f"**File Path:** {resume.get('file_path', 'Not available').split('/')[-1]}"
            )
            st.markdown(f"**Phone Number:** {resume.get('phone', 'Not available')}")
            st.markdown(f"**Score:** {resume['score']}")
            if st.checkbox("Show Skills", key=f"skills_{resume['resume_id']}"):
                skills = resume.get("skills", [])
                st.markdown(", ".join(skills), unsafe_allow_html=True)
            if st.button("Download Resume", key=f"download_{resume['resume_id']}"):
                download_resume(resume["resume_id"], headers)


def show_upload_cv():
    st.header("Upload Your CVs")

    # Check for authentication token
    token = st.session_state.get("token")
    if not token:
        st.error("You need to log in to view this page.")
        return

    # File uploader widget
    uploaded_files = st.file_uploader(
        "Choose CV files", accept_multiple_files=True, type="pdf", key="file_uploader"
    )

    # Upload button to send files to the backend
    if st.button("Upload Files"):
        if uploaded_files:
            uploaded_resumes = []
            for uploaded_file in uploaded_files:
                files = {
                    "resume_files": (
                        uploaded_file.name,
                        uploaded_file,
                        "application/pdf",
                    )
                }
                response = requests.post(
                    "http://localhost:8000/resumes/",
                    files=files,
                    headers={"Authorization": f"Bearer {token}"},
                )
                if response.status_code == 401:
                    st.error("Session expired. Please log in again.")
                    # Assuming perform_logout is a function defined elsewhere that handles logging out
                    perform_logout()
                    return
                if response.status_code == 201:
                    uploaded_resumes.append(response.json())
                else:
                    st.error(
                        f"Failed to upload {uploaded_file.name}. Status: {response.status_code}"
                    )

            if uploaded_resumes:
                st.success(f"Successfully uploaded {len(uploaded_resumes)} resumes.")
                for resume in uploaded_resumes:
                    st.json(resume)
                st.cache_data.clear()
            else:
                st.error("No resumes were uploaded successfully.")
        else:
            st.warning("No files selected. Please select files to upload.")


# Cache the resumes data to avoid repetitive requests
@st.cache_data()
def fetch_resumes(headers):
    response = requests.get("http://localhost:8000/resumes", headers=headers)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        st.error("Session expired. Please log in again.")
        perform_logout()
    elif response.status_code == 404:
        st.error("No resumes found.")
    else:
        return None


def highlight_skills(skills, search_query):
    highlighted_skills = []
    for skill in skills:
        # Check if the skill contains any part of the search query
        if any(query in skill.lower() for query in search_query):
            # Highlight skill with specific style
            highlighted_skill = (
                f'<span style="background-color:yellow;color:red;">{skill}</span>'
            )
        else:
            highlighted_skill = skill
        highlighted_skills.append(highlighted_skill)
    return ", ".join(
        highlighted_skills
    )  # Return a string with all skills, highlighted when necessary


def show_explore_data():
    st.header("Explore Stored Resumes")
    search_query = set(st.text_input("Search resumes by skills").lower().split())

    token = st.session_state.get("token")
    if not token:
        st.error("You need to log in to view this page.")
        return

    headers = {"Authorization": f"Bearer {token}"}
    resumes = fetch_resumes(headers)

    if resumes:
        selected_resumes = []
        for idx, resume in enumerate(resumes, start=1):
            skills = resume.get("skills", [])
            if search_query and not any(
                query in skill.lower() for skill in skills for query in search_query
            ):
                continue  # Skip resumes that do not match the search query

            with st.expander(
                f"Resume Number {idx} - Uploaded on: {datetime.fromisoformat(resume['upload_date'].replace('Z', '')).strftime('%d %b %Y %H:%M')}"
            ):
                st.markdown(f"**Category:** {resume['category']}")
                st.markdown(f"**Email:** {resume.get('email', 'Not available')}")
                st.markdown(
                    f"**File Path:** {resume.get('file_path', 'Not available').split('/')[-1]}"
                )
                st.markdown(f"**Phone Number:** {resume.get('phone', 'Not available')}")

                if st.checkbox("Show Skills", key=f"skills_{resume['resume_id']}"):
                    st.markdown(
                        highlight_skills(skills, search_query), unsafe_allow_html=True
                    )

                if st.checkbox("Select for deletion", key=resume["resume_id"]):
                    selected_resumes.append(resume["resume_id"])

                if st.button("Download Resume", key=f"download_{resume['resume_id']}"):
                    download_resume(resume["resume_id"], headers)

        if selected_resumes and st.button("Delete Selected Resumes"):
            delete_resumes(selected_resumes, headers)
            # show seccufull message
            st.success(f"Successfully deleted {len(selected_resumes)} resumes.")
    else:
        st.write("No resumes found.")


def download_resume(resume_id, headers):
    """Download a resume by ID."""
    response = requests.get(
        f"http://localhost:8000/resumes/files/{resume_id}", headers=headers, stream=True
    )
    if response.status_code == 200:
        content_disposition = response.headers.get("content-disposition")
        filename = (
            unquote(content_disposition.split("filename*=")[1].split("''")[1])
            if "filename*=" in content_disposition
            else "downloaded_resume.pdf"
        )
        st.download_button(
            "Click to Download",
            response.content,
            file_name=filename,
            mime="application/pdf",
        )
    else:
        st.error(f"Failed to download resume: {response.status_code}")


def delete_resumes(selected_resumes, headers):
    """Delete selected resumes."""
    response = requests.delete(
        "http://localhost:8000/delete-resumes", json=selected_resumes, headers=headers
    )
    if response.status_code == 204:
        st.success(f"Successfully deleted {len(selected_resumes)} resumes.")
        st.cache_data.clear()
        st.rerun()
    else:
        st.error(
            f"Failed to delete resumes. Status Code: {response.status_code}, Detail: {response.text}"
        )


#! this if i want to delete all resumes
# def show_explore_data():
#     st.header("Explore Stored Resumes")
#     search_query = set(st.text_input("Search resumes by skills").lower().split())

#     token = st.session_state.get("token")
#     if not token:
#         st.error("You need to log in to view this page.")
#         return

#     headers = {"Authorization": f"Bearer {token}"}
#     resumes = fetch_resumes(headers)

#     if resumes:
#         all_resume_ids = [resume["resume_id"] for resume in resumes]
#         selected_resumes = []
#         display_resumes = []

#         for resume in resumes:
#             skills = resume.get("skills", [])
#             if search_query and not any(
#                 query in skill.lower() for skill in skills for query in search_query
#             ):
#                 continue  # Skip resumes that do not match the search query
#             display_resumes.append(resume)

#         if display_resumes:
#             for resume in display_resumes:
#                 resume_id = resume["resume_id"]
#                 upload_date = datetime.fromisoformat(
#                     resume["upload_date"].replace("Z", "")
#                 )
#                 formatted_date = upload_date.strftime("%d %b %Y %H:%M")
#                 fileName = resume.get("file_path", "Not available").split("/")[-1]

#                 with st.expander(f"Resume Number - Uploaded on: {formatted_date}"):
#                     st.markdown(f"**Category:** {resume['category']}")
#                     st.markdown(f"**Email:** {resume.get('email', 'Not available')}")
#                     st.markdown(f"**File Path:** {fileName}")
#                     st.markdown(
#                         f"**Phone Number:** {resume.get('phone', 'Not available')}"
#                     )

#                     if st.checkbox(
#                         "Show Skills", key=f"skills_{resume_id}", value=False
#                     ):
#                         highlighted_skills = highlight_skills(skills, search_query)
#                         st.markdown(highlighted_skills, unsafe_allow_html=True)

#                     if st.checkbox("Select for deletion", key=resume_id):
#                         selected_resumes.append(resume_id)

#             if st.button("Delete All Displayed Resumes"):
#                 delete_response = requests.delete(
#                     "http://localhost:8000/delete-resumes",
#                     json=all_resume_ids,
#                     headers={
#                         "Authorization": f"Bearer {token}",
#                         "Content-Type": "application/json",
#                     },
#                 )
#                 if delete_response.status_code == 204:
#                     st.success("Successfully deleted all displayed resumes.")
#                     st.experimental_rerun()
#                 else:
#                     st.error(
#                         f"Failed to delete resumes. Status: {delete_response.status_code}, Detail: {delete_response.text}"
#                     )

#         else:
#             st.write("No resumes matched the criteria or all were deleted.")
#     else:
#         if resumes is None:
#             st.error("Failed to fetch resumes. Please try again.")
#         else:
#             st.write("No resumes found.")


import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px


def show_visualize_data():
    st.header("Visualize Data")
    st.write(
        "This section allows visualization of resume data in various interactive charts and diagrams."
    )

    token = st.session_state.get("token")
    if not token:
        st.error("You need to log in to view this page.")
        return

    headers = {"Authorization": f"Bearer {token}"}
    resumes = fetch_resumes(headers)

    if resumes:
        df = pd.DataFrame(resumes)
        df["file_path"] = df["file_path"].str.split("/").str[-1]

        if "upload_date" in df.columns:
            df["upload_date"] = pd.to_datetime(df["upload_date"])
            df["upload_date_formatted"] = df["upload_date"].dt.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        # don't show the resume_id column
        df.drop(columns=["resume_id"], inplace=True)
        st.write("Here's a preview of the resumes data:", df)

        # Interactive Plot: Distribution of Resume Categories
        if "category" in df.columns:
            plot_type = st.radio(
                "Choose chart type for category distribution:",
                ("Histogram", "Pie Chart"),
            )
            if plot_type == "Histogram":
                category_count = df["category"].value_counts()
                fig_histogram = px.bar(
                    category_count,
                    labels={"index": "Category", "value": "Count"},
                    title="Histogram of Resume Categories",
                    color=category_count.index,
                    # show information on hover
                    hover_data={"value": True},
                    color_discrete_sequence=px.colors.qualitative.Set1,
                )
                st.plotly_chart(fig_histogram)
            elif plot_type == "Pie Chart":
                fig_pie = px.pie(
                    df, names="category", title="Pie Chart of Resume Categories"
                )
                st.plotly_chart(fig_pie)

        # Interactive Plot: Count of Resumes by Upload Date
        if "upload_date" in df.columns:
            st.subheader("Resume Uploads Over Time")
            fig_date = px.histogram(
                df,
                x="upload_date_formatted",
                nbins=20,
                # add gap between bars for better visibility
                title="Resume Uploads Over Time",
                labels={"upload_date_formatted": "Upload Date"},
            )
            st.plotly_chart(fig_date)

            # Further plots can be added based on additional data available
            if "category" in df.columns and "upload_date" in df.columns:
                fig_scatter = px.scatter(
                    df,
                    x="upload_date",
                    y="category",
                    color="category",
                    title="Upload Date by Category",
                )
                st.plotly_chart(fig_scatter)
                # Skill search and distribution

    else:
        st.write("No resume data available for visualization.")
