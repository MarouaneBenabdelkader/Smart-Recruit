import re


def extract_info(text):
    # Extract email addresses using a regular expression
    email = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    email = email.group() if email else None
    phone = re.search(r"\b\d{2}\s?\d{2}\s?\d{2}\s?\d{2}\s?\d{2}\b", text)
    phone = phone.group() if phone else None
    # Extract phone numbers using a regular expression
    if phone is None:
        phone = re.search(
            r"(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\b\d{7}\b|\b\d{10}\b)", text
        )
        phone = phone.group() if phone else None

    return {"email": email, "phone": phone}
