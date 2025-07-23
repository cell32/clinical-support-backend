
from fastapi import FastAPI, Body, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.rules_engine import suggest_diagnosis as suggest_rules_diagnosis
from app.ai_engine import suggest_diagnosis_ai
from app.drug_checker import check_interactions
from app.extractor import extract_symptoms
from app.rules_engine import suggest_treatment as suggest_rules_treatment
from app.ai_engine import suggest_treatment_ai  # AI fallback

from pydantic import BaseModel
from typing import List

app = FastAPI()

#Correct CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
       "https://clinical-support-tool-frontend.onrender.com",],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class DiagnosisRequest(BaseModel):
    text: str

class TreatmentRequest(BaseModel):
    diagnosis: List[str]

@app.get("/")
def read_root():
    return {"message": "Clinical Decision Support Tool is running!"}

@app.post("/api/diagnosis")
def diagnosis(request: DiagnosisRequest):
    user_input = request.text

    # 1. Extract keywords from natural language
    extracted_symptoms = extract_symptoms(user_input)

    # 2. Run rules engine
    rules_result = suggest_rules_diagnosis(" ".join(extracted_symptoms))  # re-join for pattern match
    rules_output = [{"diagnosis": diag, "confidence": "high"} for diag in rules_result] if rules_result else []

    if not rules_output:
        ai_output = suggest_diagnosis_ai(user_input)
        return {"ai_based_diagnosis": ai_output, 
                "message": "No Rules-based suggested diagnosis was found. Using AI-based suggested diagnosis instead (review recommended)."}
    else:
        return{"rules_based_diagnosis": rules_output}

@app.post("/api/suggestedTreatment")
def suggested_treatment(request: TreatmentRequest):
    print("Received diagnoses:", request.diagnosis)
    diagnoses = request.diagnosis

    # 1. Try rules-based treatment suggestions
    rules_based_treatments = suggest_rules_treatment(diagnoses)

    if rules_based_treatments:
        return {
            "rules_based_treatment": rules_based_treatments,
            "message": "Rules-based treatment found based on provided diagnosis."
        }
    else:
        # 2. Fallback to AI-based treatment suggestion
        ai_treatment = suggest_treatment_ai(diagnoses[0]) if diagnoses else []
        return {
            "ai_based_treatment": ai_treatment,
            "message": "No rules-based treatment found. Using AI-based suggestion instead (review recommended)."
        }
    
    