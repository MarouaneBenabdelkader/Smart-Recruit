import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import re


def clean_text(text):
    """Cleans the extracted text."""
    text = text.replace("\n", " ")  # Replace new lines with spaces
    text = re.sub(r"\s+", " ", text)  # Replace multiple spaces with a single space
    text = re.sub(
        r"\.\s+", ". ", text
    )  # Ensure space after periods, enhancing sentence recognition
    text = text.strip()  # Remove leading and trailing spaces
    return text


def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file using both direct extraction and OCR as fallback."""
    try:
        with fitz.open(pdf_path) as pdf:
            full_text = ""
            for page in pdf:
                text = page.get_text()
                if not text:  # If no text found, use OCR
                    pix = page.get_pixmap()
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    text = pytesseract.image_to_string(img)
                full_text += text
            return clean_text(full_text)
    except Exception as e:
        print(f"Failed to process {pdf_path}: {str(e)}")
        return None
