
# app/extractor.py

import re

SYMPTOM_KEYWORDS = [
    "fever", "cough", "headache", "sore throat", "chest pain", "fatigue",
    "nausea", "vomiting", "dizziness", "shortness of breath"
]

def extract_symptoms(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    found = []

    for keyword in SYMPTOM_KEYWORDS:
        if keyword in text:
            found.append(keyword)

    return found