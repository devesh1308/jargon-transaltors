import os
import pickle
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 1. Setup the folder paths for the NEW clean architecture
# Since this script lives in backend/scripts/, we go UP one level to get the backend root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models")
CONFIG_DIR = os.path.join(BASE_DIR, "config")

# Ensure the new directories exist
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(CONFIG_DIR, exist_ok=True)

# 2. The Expanded Hackathon Training Data
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

# 3. Split the data to test accuracy (80% Train, 20% Test)
X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)

print("🧠 Building the Linear SVC ML Pipeline...")
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english')),
    ('clf', LinearSVC())
])

# 4. Train on 80% and Grade the Test
pipeline.fit(X_train, y_train)
predictions = pipeline.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print("\n" + "="*40)
print(f"🏆 INTERNAL SVC TEST ACCURACY: {accuracy * 100:.1f}%")
print("="*40 + "\n")

# 5. Pro Move: Retrain on 100% of the data so the final model is as smart as possible
print("📈 Retraining on 100% of data for maximum performance...")
pipeline.fit(texts, labels)

# 6. Save the pipeline directly to the models folder with professional naming
pipeline_path = os.path.join(MODEL_DIR, "linear_svc.pkl")
with open(pipeline_path, "wb") as f:
    pickle.dump(pipeline, f)

# 7. Recreate the dictionary and save to config
clause_dictionary = {
    "Safe": "✅ Standard practice. Protects both parties fairly.",
    "Caution": "⚠️ Pay attention.",
    "Predatory": "🚨 RED FLAG. Highly illegal or heavily favors the other party. Negotiate immediately."
}

with open(os.path.join(CONFIG_DIR, "dictionary.json"), "w", encoding="utf-8") as f:
    json.dump(clause_dictionary, f, indent=4)

print(f"✅ SUCCESS! linear_svc.pkl saved to {MODEL_DIR}")