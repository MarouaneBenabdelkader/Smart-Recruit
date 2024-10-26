import spacy
from elasticsearch import Elasticsearch
import pytesseract
import pickle
import joblib
import os
import requests  # For handling HTTP-related errors


class NLPResources:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls._load_resources()
        return cls._instance

    @staticmethod
    def _load_resources():
        resources = {}

        # Load OCR tool
        try:
            print("Loading OCR tool...")
            if not os.path.exists(r"C:\Program Files\Tesseract-OCR\tesseract.exe"):
                raise FileNotFoundError("Tesseract executable not found.")
            pytesseract.pytesseract.tesseract_cmd = (
                r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            )
            print("OCR tool loaded.")
        except Exception as e:
            print(f"Error loading OCR tool: {e}")
            raise

        # Load Spacy NLP model
        try:
            print("Loading Spacy NLP model...")
            resources["nlp"] = spacy.load("en_core_web_lg")
            print("Spacy model loaded.")
        except OSError as e:
            print(f"Error loading Spacy model: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error loading Spacy model: {e}")
            raise

        # Load Matcher
        try:
            print("Loading Matcher...")
            with open("./assets/matcher_patterns.pkl", "rb") as f:
                resources["matcher"] = pickle.load(f)
            print("Matcher loaded.")
        except FileNotFoundError as e:
            print(f"Error loading Matcher: File not found. {e}")
            raise
        except pickle.PickleError as e:
            print(f"Error loading Matcher: Pickle error. {e}")
            raise
        except Exception as e:
            print(f"Unexpected error loading Matcher: {e}")
            raise

        # Connect to Elasticsearch
        try:
            print("Connecting to Elasticsearch...")
            resources["es"] = Elasticsearch(["http://localhost:9200/"])
            if not resources["es"].ping():
                raise ValueError("Connection to Elasticsearch failed.")
            print("Elasticsearch connected.")
        except requests.ConnectionError as e:
            print(f"Error connecting to Elasticsearch: Connection error. {e}")
            raise
        except ValueError as e:
            print(f"Error connecting to Elasticsearch: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error connecting to Elasticsearch: {e}")
            raise

        # Load TF-IDF Vectorizer
        try:
            print("Loading TF-IDF Vectorizer...")
            resources["vectorizer"] = joblib.load("./assets/tfidf_vectorizer.joblib")
            print("Vectorizer loaded.")
        except FileNotFoundError as e:
            print(f"Error loading TF-IDF Vectorizer: File not found. {e}")
            raise
        except joblib.JoblibException as e:
            print(f"Error loading TF-IDF Vectorizer: Joblib error. {e}")
            raise
        except Exception as e:
            print(f"Unexpected error loading TF-IDF Vectorizer: {e}")
            raise

        # Load SVM Model
        try:
            print("Loading SVM Model...")
            resources["model"] = joblib.load("./assets/svm_model.joblib")
            print("Model loaded.")
        except FileNotFoundError as e:
            print(f"Error loading SVM Model: File not found. {e}")
            raise
        except joblib.JoblibException as e:
            print(f"Error loading SVM Model: Joblib error. {e}")
            raise
        except Exception as e:
            print(f"Unexpected error loading SVM Model: {e}")
            raise

        return resources
