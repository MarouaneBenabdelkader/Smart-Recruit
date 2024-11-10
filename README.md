# Table of Contents
- [Application Architecture Overview](#application-architecture-overview)
- [Backend Startup Process](#backend-startup-process)
- [Login Page](#login-page)
- [Registration Page](#registration-page)
- [Resume Ranker Page](#resume-ranker-page)
- [Upload CV Page](#upload-cv-page)
- [Explore Stored Resumes Page](#explore-stored-resumes-page)
- [Data Visualization Page](#data-visualization-page)
- [Project Setup and Usage Guide](#project-setup-and-usage-guide)
  - [Prerequisites](#prerequisites)
  - [Step 1: Configure MongoDB URL](#step-1-configure-mongodb-url)
  - [Step 2: Run Elasticsearch Container in Docker](#step-2-run-elasticsearch-container-in-docker)
  - [Step 3: Set Pytesseract Path](#step-3-set-pytesseract-path)
  - [Step 4: Run the Backend Server](#step-4-run-the-backend-server)
  - [Step 5: Run Streamlit Frontend](#step-5-run-streamlit-frontend)

# Application Architecture Overview

## Application Architecture Overview
Below is an architecture diagram that illustrates the overall structure and interaction between the frontend, backend, and supporting services of the SmartRecruit application:

![image](https://github.com/user-attachments/assets/2d4c3636-acf1-4510-b920-35e163ae0e33)

### Explanation:
- **Frontend**: The user interacts with the application through a web browser, which is supported by the Streamlit framework for the UI.
- **Backend**: The backend is built using FastAPI to provide RESTful web services. It handles requests from the frontend, processes data, and communicates with external services.
- **Elasticsearch**: Used for indexing and searching resumes, running within a Docker container to manage scalable search operations.
- **MongoDB Atlas**: A cloud-based database where user and resume data are stored. The backend interacts with MongoDB using the `pymongo` library.
- **Docker**: Manages the containerization of services like Elasticsearch to ensure a consistent and scalable environment.

## Backend Startup Process

![image](https://github.com/user-attachments/assets/3102e754-50f2-49fc-81a6-82620babf8c4)

 - **Matcher**: Loads patterns into spaCy's `PhraseMatcher` for extracting skills.
  - **SVM Model**: Loads the pre-trained SVM model for classifying resumes.
  - **TF-IDF Vectorizer**: Loads the TF-IDF vectorizer used to transform text into numerical vectors.
  - **OCR Tool**: Loads the OCR (Optical Character Recognition) tool to extract text from scanned PDFs.
  - **spaCy NLP Model**: Loads spaCy's NLP model for various natural language processing tasks such as tokenization, dependency parsing, and named entity recognition (NER).

## Login Page
![image](https://github.com/user-attachments/assets/59bb4f13-a4c0-40d7-90d9-33549b375dfa)

## Registration Page
![image](https://github.com/user-attachments/assets/eee062fa-4e8a-4f64-8c27-1305fd5a0998)


## Resume Ranker Page
The "Resume Ranker" page allows users to input a job description and rank stored resumes based on their relevance to the provided job description. Users can choose to include only today's resumes and specify the number of results to return. The results are displayed with scores indicating how well each resume matches the job criteria.

![image](https://github.com/user-attachments/assets/833c8eda-1902-419e-81ec-0b311e0b6aa9)

### Features of the Resume Ranker Page:
- **Job Description Input**: Users can enter detailed job descriptions to tailor the ranking process.
- **Filter Option**: Check the box to include only resumes uploaded on the current day.
- **Results Limiting**: A slider allows the user to set the number of resumes to display.
- **Ranked Resumes**: Each resume is shown with a score and upload date to help identify the most relevant candidates.

## Upload CV Page
The "Upload CV" page enables users to upload their resumes to the system. Users can drag and drop files or use the "Browse files" button to upload their documents. The page provides a status update upon successful upload.

![image](https://github.com/user-attachments/assets/60c0c0fe-8392-455b-a91e-e2e053d8b804)

## Explore Stored Resumes Page
The "Explore Stored Resumes" page allows users to browse and search through previously uploaded resumes. Users can expand each resume entry to view details such as category, contact information, and the file path. The page also includes options to show the candidate's skills or select a resume for deletion. Users can download individual resumes directly from this page.

![image](https://github.com/user-attachments/assets/f71dadf2-eb24-4f9c-b8bd-e9f31e8d6e99)

### Features of the Explore Stored Resumes Page:
- **Search Functionality**: Users can filter resumes based on skills.
- **Detailed Resume View**: Expanding a resume shows detailed information including category, email, file path, and phone number.
- **Resume Management**: Users can choose to show skills, mark a resume for deletion, or download it.

## Data Visualization Page
The "Data Visualization" page provides graphical insights into the distribution of stored resumes based on their categories. Users can choose between different chart types, such as histograms or pie charts, to view the distribution. This helps to analyze the resume data visually and understand the trends in candidate submissions.

![image](https://github.com/user-attachments/assets/13a305e2-3133-46ca-90ee-8ac978b49451)


# Project Setup and Usage Guide

Follow these steps to set up and run the project.

## Prerequisites

- [Docker](https://hub.docker.com/_/elasticsearch) (for running the Elasticsearch container)
- [MongoDB](https://www.mongodb.com/cloud/atlas/register) 
- [Pytesseract](https://github.com/tesseract-ocr/tesseract) (for OCR functionality)

## Step 1: Configure MongoDB URL
1. Open `config.py` in backend/app.
2. Locate the MongoDB URL configuration.
3. Replace the existing URL with your MongoDB connection string.

   ```python
   # Example in config.py
   mongodb_url: str = "Add your MongoDB URL here"

## Step 2: Run Elasticsearch Container in Docker

To run Elasticsearch in a Docker container, execute the following commands:

### Pull the Elasticsearch image:
```bash
docker pull docker.elastic.co/elasticsearch/elasticsearch:7.17.21
```

### Run the Elasticsearch container (replace `<your-container-name>` with the desired container name):
```bash
docker run --name <your-container-name> --net elastic -p 127.0.0.1:9200:9200 -p 127.0.0.1:9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.17.21
```

### Start the container (replace `<your-container-name>` with the name you used):
```bash
docker start <your-container-name>
```

This setup will run an Elasticsearch container that listens on `127.0.0.1` on ports `9200` and `9300`.

## Step 3: Set Pytesseract Path

Open `ressource/nlp_loader.py`.

Set the path of `pytesseract` to ensure OCR functionalities work correctly.

### Example in `ressource/nlp_loader.py`:
```python
pytesseract.pytesseract.tesseract_cmd = (r"path_to_your_tesseract_executable")
```

Replace `path_to_your_tesseract_executable` with the actual path to the Tesseract executable on your system.

## Step 4: Run the Backend Server

Navigate to the backend directory:

```bash
cd .\backend\app\
```

### Install the required Python packages:
```bash
pip install -r requirements.txt
```

### Start the backend server using Uvicorn:
```bash
uvicorn main:app --reload
```

This command runs the server in development mode with auto-reloading enabled.



```markdown
## Step 5: Run Streamlit Frontend

Navigate to the frontend directory:

```bash
cd .\frontend\
```

### Install the required Python packages:
```bash
pip install -r requirements.txt
```

### Start the Streamlit frontend:
```bash
streamlit run main.py

