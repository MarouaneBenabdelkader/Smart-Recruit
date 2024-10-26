import spacy
from spacy.tokens import Span
from spacy.util import filter_spans


def extract_skills(text, matcher):
    nlp = spacy.blank("en")
    doc = nlp(text.lower())
    matches = matcher(doc)
    spans = [Span(doc, start, end, label="SKILL") for match_id, start, end in matches]
    filtered_spans = filter_spans(spans)
    unique_skills = {span.text.strip(". ") for span in filtered_spans}
    return list(unique_skills)
