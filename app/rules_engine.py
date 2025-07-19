# rules_engine.py

import re

def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)  # remove punctuation
    return text

def suggest_diagnosis(user_input):
    user_input = user_input.lower()

    rules = {
        ("fever", "cough"): "Possible Flu",
        ("headache", "sore throat"): "Possible Infection",
        ("chest pain"): "Possible Heart Issue",
        ("shortness of breath",): "Possible Respiratory Issue",
        ("fatigue",  "dizziness"): "Possible Anemia",
        ("nausea",  "vomiting"): "Possible Gastroenteritis",
        ("back pain"): "Possible Musculoskeletal Issue",
        ("rash", "fever"): "Possible Measles or Viral Infection"
    }

    matched_diagnoses = []

    for symptom_keywords, diagnosis in rules.items():
        if all(keyword in user_input for keyword in symptom_keywords):
            matched_diagnoses.append(diagnosis)

    return matched_diagnoses

treatment_rules = {
    "Possible Flu": ["Rest", "Hydration", "Paracetamol"],
    "Possible Infection": ["Antibiotics (as prescribed)", "Hydration"],
    "Possible Heart Issue": ["Immediate medical attention", "Aspirin (consult doctor)"],
}

def suggest_treatment(diagnosis_list):
    treatments = []
    for diagnosis in diagnosis_list:
        if diagnosis in treatment_rules:
            treatments.extend(treatment_rules[diagnosis])
    return list(set(treatments)) 