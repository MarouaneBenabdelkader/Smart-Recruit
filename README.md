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
