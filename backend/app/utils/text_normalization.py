import spacy
import re


def normalize_text(text, nlp):
    text = text.lower()
    text = re.sub(r"<.*?>", " ", text)
    doc = nlp(text)
    tokens = [
        token.lemma_
        for token in doc
        if not token.is_stop and not token.is_punct and not token.is_space
    ]
    return " ".join(tokens)
