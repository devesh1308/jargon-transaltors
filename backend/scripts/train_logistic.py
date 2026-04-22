import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# 1. Setup the folder paths for the NEW clean architecture
# Since this script lives in backend/scripts/, we go UP one level to get the backend root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models")

# Ensure the new directory exists
os.makedirs(MODEL_DIR, exist_ok=True)

# The Hackathon Training Data
training_data = [
    # --- SAFE CLAUSES ---
    ("RESIDENTIAL LEASE AGREEMENT.", "Safe"),
    ("LEAVE AND LICENSE AGREEMENT TERMS.", "Safe"),
    ("This Leave and License Agreement is granted for a period of 11 months for strictly residential purposes.", "Safe"),
    ("RENT: Tenant agrees to pay rent per month due on the 1st.", "Safe"),
    ("The security deposit shall be refunded within 30 days of vacating the premises.", "Safe"),
    ("INSURANCE: Tenant must purchase renters insurance with minimum liability.", "Safe"),
    ("UTILITIES: Tenant agrees to pay for all utility charges including water, gas, and electricity.", "Safe"),
    ("NOTICE: Landlord will provide 24 hours notice before entering the property.", "Safe"),
    ("SUBLETTING: Tenant shall not sublet the property without written permission from landlord.", "Safe"),
    ("Tenant has the right to quietly enjoy the premises.", "Safe"),
    
    # --- CAUTION CLAUSES ---
    ("MAINTENANCE PROTOCOL: However, the tenant is responsible for all routine maintenance and minor repairs.", "Caution"),
    ("CLEANING: Tenant agrees to pay 200 dollars cleaning fee regardless of property condition.", "Caution"),
    ("WAIVER: Tenant waives right to a jury trial in any eviction proceeding.", "Caution"),
    ("DISPUTE RESOLUTION: Any dispute between landlord and tenant must go to binding arbitration.", "Caution"),
    ("A late fee of Rs 500 per day will be charged for delayed rent.", "Caution"),
    ("Furthermore, failure to pay rent on time will result in severe penalties, and a late fee of Rs 500 per day will be charged for delayed rent.", "Caution"),
    ("LOCK-IN AND PENALTIES: The Licensee is bound by a strict 11-month lock-in period.", "Caution"),
    
    # --- PREDATORY CLAUSES ---
    ("FINANCIAL REVISIONS: Landlord reserves the right to increase rent by any amount with 24 hours notice.", "Predatory"),
    ("Landlord reserves the right to increase rent by any amount with 24 hours notice.", "Predatory"),
    ("LATE FEE: If rent is one day late, tenant agrees to pay 20 percent of monthly rent as penalty.", "Predatory"),
    ("INSPECTION RIGHTS: The landlord reserves the right to enter the premises at any time without prior intimation to inspect for damages.", "Predatory"),
    ("REPAIRS: Tenant is responsible for all repairs including major structural damage and HVAC.", "Predatory"),
    ("Upon vacating, the tenant must pay a non-refundable painting and cleaning fee equivalent to two months of rent.", "Predatory"),
    ("TERMINATION: Landlord may terminate lease with 7 days notice for any reason.", "Predatory"),
    ("GUESTS: Tenant cannot have guests stay for more than 3 consecutive days.", "Predatory"),
    ("The security deposit is strictly non-refundable under all circumstances.", "Predatory"),
    ("Landlord may withhold the entire deposit if the tenant breaks the 11-month lock-in period.", "Predatory")
]

texts = [item[0] for item in training_data]
labels = [item[1] for item in training_data]

print("🧠 Building the Logistic Regression ML Pipeline...")
# The Logistic Regression approach (with balanced class weights)
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english', ngram_range=(1, 2))),
    ('clf', LogisticRegression(class_weight='balanced'))
])

pipeline.fit(texts, labels)

# Save the pipeline directly to the new models folder with professional naming
pipeline_path = os.path.join(MODEL_DIR, "logistic_regression.pkl")
with open(pipeline_path, "wb") as f:
    pickle.dump(pipeline, f)

print(f"✅ SUCCESS! logistic_regression.pkl saved to {MODEL_DIR}")