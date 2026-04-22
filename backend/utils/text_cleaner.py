import re

def clean_and_split_text(text: str) -> list:
    """Splits text into individual sentences and cleans whitespace."""
    # Split by newlines OR periods followed by spaces
    raw_clauses = re.split(r'\.\s+|\n+', text)
    
    cleaned_clauses = []
    for clause in raw_clauses:
        cleaned = clause.strip()
        # Only keep actual sentences (skip empty strings or tiny numbers)
        if len(cleaned) > 20: 
            # Add the period back for clean frontend display
            if not cleaned.endswith('.'):
                cleaned += '.'
            cleaned_clauses.append(cleaned)
            
    return cleaned_clauses

def preprocess_for_model(text: str) -> str:
    """Basic cleanup before feeding to the ML model."""
    return text.lower().strip()