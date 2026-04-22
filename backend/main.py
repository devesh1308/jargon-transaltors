from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pdfplumber
import pickle
import json
import os
import re
import traceback

app = FastAPI(title="ClauseGuard Ensemble API", version="3.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# UPDATED PATH: Pointing to the new config folder
DICT_PATH = os.path.join(BASE_DIR, "config", "dictionary.json")

# Global variables for BOTH models (Professional Naming)
svc_pipeline = None
logistic_pipeline = None
clause_dictionary = {}

@app.on_event("startup")
def load_ml_assets():
    global svc_pipeline, logistic_pipeline, clause_dictionary
    try:
        # UPDATED PATHS: Pointing to the new models folder with renamed files
        with open(os.path.join(BASE_DIR, "models", "linear_svc.pkl"), "rb") as f:
            svc_pipeline = pickle.load(f)
        with open(os.path.join(BASE_DIR, "models", "logistic_regression.pkl"), "rb") as f:
            logistic_pipeline = pickle.load(f)
            
        with open(DICT_PATH, "r") as f:
            clause_dictionary = json.load(f)
        print("✅ ENSEMBLE ACTIVE: Linear SVC & Logistic Regression pipelines loaded!")
    except Exception as e:
        print(f"⚠️ Failed to load ML models. Error: {e}")

@app.get("/")
async def root():
    return {"message": "ClauseGuard Offline Ensemble API is active."}

@app.get("/health")
async def health():
    if svc_pipeline is None or logistic_pipeline is None:
        raise HTTPException(status_code=503, detail="Models not loaded")
    return {"status": "healthy", "mode": "Ensemble Voting"}

class TextRequest(BaseModel):
    text: str

# --- THE ENSEMBLE LOGIC ENGINE ---
def get_ensemble_prediction(text_input: str) -> str:
    """Passes text to both models and returns the safest (highest risk) vote."""
    # Convert to lowercase and strip whitespace for the models
    clean_input = text_input.lower().strip()
    
    pred_svc = svc_pipeline.predict([clean_input])[0]
    pred_logistic = logistic_pipeline.predict([clean_input])[0]
    
    # Voting Logic: The highest risk vote always wins
    if pred_svc == "Predatory" or pred_logistic == "Predatory":
        return "Predatory"
    elif pred_svc == "Caution" or pred_logistic == "Caution":
        return "Caution"
    else:
        return "Safe"


# --- ENDPOINT 1: PDF FILE UPLOAD ---
@app.post("/predict")
async def predict_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    if svc_pipeline is None or logistic_pipeline is None:
        raise HTTPException(status_code=503, detail="ML Engine offline.")

    # Secure temp file path
    temp_path = f"temp_{file.filename}"
    
    try:
        # Save temp file
        content = await file.read()
        with open(temp_path, "wb") as f:
            f.write(content)

        results = []
        
        # Extract text using pdfplumber
        with pdfplumber.open(temp_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    # FIX 1: Glue PDF line-breaks back into a single paragraph
                    text = text.replace('\n', ' ')
                    # FIX 2: Prevent abbreviations from splitting sentences
                    text = text.replace('Rs. ', 'Rs ')
                    text = text.replace('Mr. ', 'Mr ')
                    text = text.replace('Mrs. ', 'Mrs ')
                    
                    # Smart Split: Now ONLY split by periods followed by spaces
                    raw_clauses = re.split(r'\.\s+', text)
                    
                    for clause in raw_clauses:
                        # Clean up extra spaces from PDF extraction
                        clean = re.sub(r'\s+', ' ', clause).strip()
                        
                        # Only analyze actual sentences (skip page numbers/headers)
                        if len(clean) > 20:
                            # Add period back for nice UI display
                            if not clean.endswith('.'):
                                clean += '.'
                            
                            # Predict using the Ensemble Model
                            final_risk = get_ensemble_prediction(clean)
                            translation = clause_dictionary.get(final_risk, "Analysis unavailable.")
                            
                            results.append({
                                "original_text": clean,
                                "risk": final_risk,
                                "translation": translation
                            })
                            
        return {
            "status": "success",
            "filename": file.filename,
            "total_clauses": len(results),
            "clauses": results
        }
        
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"PDF Processing Error: {str(e)}")
    finally:
        # Always delete the temp file, even if an error occurs!
        if os.path.exists(temp_path):
            os.remove(temp_path)


# --- ENDPOINT 2: DIRECT TEXT UPLOAD ---
@app.post("/predict-text")
async def predict_text_direct(request: TextRequest):
    if svc_pipeline is None or logistic_pipeline is None:
        raise HTTPException(status_code=503, detail="ML Engine offline.")

    try:
        # Apply the exact same smart fixes for direct text
        text = request.text.replace('\n', ' ')
        text = text.replace('Rs. ', 'Rs ')
        text = text.replace('Mr. ', 'Mr ')
        text = text.replace('Mrs. ', 'Mrs ')
        
        raw_clauses = re.split(r'\.\s+', text)
        results = []
        
        for clause in raw_clauses:
            clean = re.sub(r'\s+', ' ', clause).strip()
            if len(clean) > 20:
                if not clean.endswith('.'):
                    clean += '.'
                    
                final_risk = get_ensemble_prediction(clean)
                translation = clause_dictionary.get(final_risk, "Analysis unavailable.")

                results.append({
                    "original_text": clean, 
                    "risk": final_risk,
                    "translation": translation
                })

        return {
            "status": "success",
            "filename": "Direct Text Input", 
            "total_clauses": len(results),
            "clauses": results
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"ML Error: {str(e)}")