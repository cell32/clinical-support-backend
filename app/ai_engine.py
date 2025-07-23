""" The entire code will be commented out. if adding feature in the future, un-commented it so that it can be
tested agains OLLAMA which is running locally and DO NOT USE OPENAI whihc 
makes a API call. This will only be used due to the constrain to run it on RENDER """
# from ollama import Client
# import json
# import re

# from app.rules_engine import suggest_treatment

# client = Client(host='http://localhost:11434') # since app is in WLS venv and Ollama in windows this does not work
# # client = Client(host='http://172.18.64.1:11434')

# # Modified function and Prompt modified so that Ollama handles plain text better that structure comma separated keywords
# def suggest_diagnosis_ai(user_input): 
#     system_msg = (
#         "You are a clinical decision support assistant. "
#         "Your job is to suggest possible diagnoses based on symptoms provided. "
#         "You must only return a valid JSON array without any explanations, markdown, or extra text. "
#         "Example output:\n"
#         '[{"diagnosis": "Flu", "confidence": "high"}, {"diagnosis": "Common Cold", "confidence": "medium"}]'
#     )

#     prompt = f"""
#     Based on the following symptom description, suggest possible diagnoses with a confidence score.

#     Symptoms:
#     \"\"\"{user_input}\"\"\"
#     """

#     try:
#         response = client.chat(
#             model="llama3:8b",
#             messages=[
#                 {"role": "system", "content": system_msg},
#                 {"role": "user", "content": prompt}
#             ],

#             # These options added after some reserach to improve the model (temporal changes)
#             options={
#                 "temperature": 0.2,    # Strictly factual
#                 "top_k": 20,          # Only top 20 probable tokens
#                 "seed": 42            # For reproducibility
#             }
#         )

#         raw = response["message"]["content"].strip()
#         print("\n====================")
#         print("Raw response from Ollama:")
#         print(raw)
#         print("===============================\n")

#         # Extract JSON block if the response is wrapped in backticks
#         match = re.search(r"```(?:json)?\s*(\[\s*\{.*?\}\s*\])\s*```", raw, re.DOTALL)
#         if match:
#             content = match.group(1)
#         else:
#             content = raw  # Assume the whole response is the JSON if no backticks

#         return json.loads(content)

#     except Exception as e:
#         print("Error fetching AI diagnosis:", e)
#         return [{"diagnosis": "Error processing AI diagnosis", "confidence": "low"}]
    
# def suggest_treatment_ai(diagnoses): 
#     system_msg = (
#         "You are a clinical decision support assistant. "
#         "Your job is to suggest possible treatments based on the provided list of diagnoses. "
#         "You must only return a valid JSON array without any explanations, markdown, or extra text. "
#         "Each item should follow this structure:\n"
#         '[{"diagnosis": "Flu", "possible_treatments": ["Rest", "Hydration", "Paracetamol"]}, {"diagnosis": "Infection", "possible_treatments": ["Antibiotics (as prescribed)", "Hydration"]}]'
#     )

#     prompt = f"""
#     Based on the following diagnoses, suggest possible treatments.
#     Include a suggestion to consult a doctor before starting any treatment.

#     Diagnoses:
#     \"\"\"{diagnoses}\"\"\"
#     """
#     try:
#         response = client.chat(
#             model="llama3:8b",
#             messages=[
#                 {"role": "system", "content": system_msg},
#                 {"role": "user", "content": prompt}
#             ],

#             # These options added after some research to improve the model (temporal changes)
#             options={
#                 "temperature": 0.3,  # Slightly higher for treatment variety (but still cautious)
#                 "top_k": 30,
#                 "seed": 42
#             }            
#         )

#         raw = response["message"]["content"].strip()
#         print("\n====================")
#         print("Raw response from Ollama:")
#         print(raw)
#         print("===============================\n")

#         # Extract JSON block if the response is wrapped in backticks
#         match = re.search(r"```(?:json)?\s*(\[\s*\{.*?\}\s*\])\s*```", raw, re.DOTALL)
#         if match:
#             content = match.group(1)
#         else:
#             content = raw  # Assume the whole response is the JSON if no backticks

#         return json.loads(content)

#     except Exception as e:
#         print("Error fetching AI diagnosis:", e)
#         return [{
#             "diagnosis": "Error",
#             "possible_treatments": ["Unable to process treatment suggestions at this time."]
#         }]

""" Using OPENAI to make a API call, use this code for Production only"""
import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Get API key with validation
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

print("DEBUG API KEY:", os.getenv("OPENAI_API_KEY"))
client = OpenAI(api_key=OPENAI_API_KEY)

def suggest_diagnosis_ai(user_input): 

    system_msg = (
        "You are a clinical decision support assistant. "
        "Your job is to suggest possible diagnoses based on symptoms provided. "
        "You must only return a valid JSON array without any explanations, markdown, or extra text. "
        "Example output:\n"
        '[{"diagnosis": "Flu", "confidence": "high"}, {"diagnosis": "Common Cold", "confidence": "medium"}]'
    )

    prompt = f"""Symptoms:
\"\"\"{user_input}\"\"\""""

    try:
        response = client.chat.completions.create(
            model="gpt-4",  # or gpt-4 if enabled
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        # raw = response['choices'][0]['message']['content'].strip()
        raw = response.choices[0].message.content.strip()
        print("OpenAI raw response:\n", raw)

        # Try direct JSON first
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            # Fallback to extract array if there's extra text
            match = re.search(r"\[(.*?)\]", raw, re.DOTALL)
            if match:
                json_data = "[" + match.group(1).strip() + "]"
                return json.loads(json_data)
            else:
                raise  # Let the outer exception handle it

    except Exception as e:
        print("OpenAI error:", e)
        return [{"diagnosis": "Error fetching AI diagnosis", "confidence": "low"}]
    

def suggest_treatment_ai(diagnoses): 
    system_msg = (
        "You are a clinical decision support assistant. "
        "Your job is to suggest possible treatments based on the provided list of diagnoses. "
        "You must only return a valid JSON array without any explanations, markdown, or extra text. "
        "Each item should follow this structure:\n"
        '[{"diagnosis": "Flu", "possible_treatments": ["Rest", "Hydration", "Paracetamol"]}, {"diagnosis": "Infection", "possible_treatments": ["Antibiotics (as prescribed)", "Hydration"]}]'
    )

    prompt = f"""
    Based on the following diagnoses, suggest possible treatments.
    Include a suggestion to consult a doctor before starting any treatment.

    Diagnoses:
    \"\"\"{diagnoses}\"\"\"
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",  # or gpt-4 if enabled
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        # raw = response['choices'][0]['message']['content'].strip()
        raw = response.choices[0].message.content.strip()
        print("OpenAI raw response:\n", raw)

        # Try direct JSON first
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            # Fallback to extract array if there's extra text
            match = re.search(r"\[(.*?)\]", raw, re.DOTALL)
            if match:
                json_data = "[" + match.group(1).strip() + "]"
                return json.loads(json_data)
            else:
                raise  # Let the outer exception handle it

    except Exception as e:
        print("Error fetching AI diagnosis:", e)
        return [{
            "diagnosis": "Error",
            "possible_treatments": ["Unable to process treatment suggestions at this time."]
        }]