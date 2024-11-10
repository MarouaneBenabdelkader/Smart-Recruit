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
```

