import os
import pickle
from sklearn.metrics import accuracy_score

# 1. Setup the folder paths for the NEW clean architecture
# Since this script lives in backend/scripts/, we go UP one level to get the backend root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models")

# 2. Load Both "Brains" (Like parallel circuits)
try:
    with open(os.path.join(MODEL_DIR, "linear_svc.pkl"), "rb") as f:
        svc_model = pickle.load(f)
    with open(os.path.join(MODEL_DIR, "logistic_regression.pkl"), "rb") as f:
        logistic_model = pickle.load(f)
    print("✅ Both Linear SVC and Logistic Regression pipelines loaded successfully!")
except Exception as e:
    print(f"❌ Error loading models: {e}")
    print("Ensure both linear_svc.pkl and logistic_regression.pkl are in the models/ folder.")
    exit()

# 3. The Unseen Pop Quiz Dataset
test_dataset = [
    # Safe Clauses
    ("The security deposit shall be refunded within 30 days of vacating the premises.", "Safe"),
    ("Tenant has the right to quietly enjoy the premises.", "Safe"),
    ("The landlord shall provide a minimum 30-day written notice prior to any rent revision.", "Safe"),
    
    # Caution Clauses
    ("However, the tenant is responsible for all routine maintenance and minor repairs.", "Caution"),
    ("Tenant must pay for professional cleaning upon move-out regardless of condition.", "Caution"),
    ("A late fee of Rs. 500 per day will be charged for delayed rent.", "Caution"),
    
    # Predatory Clauses
    ("The landlord reserves the right to enter the premises at any time without prior intimation.", "Predatory"),
    ("The security deposit is strictly non-refundable under all circumstances.", "Predatory"),
    ("Landlord may withhold the entire deposit if the tenant breaks the 11-month lock-in period.", "Predatory"),
    ("The tenant must pay a non-refundable painting fee equivalent to two months of rent.", "Predatory")
]

texts = [item[0] for item in test_dataset]
true_labels = [item[1] for item in test_dataset]

# 4. Get predictions from BOTH models
print("📝 Running the Face-Off...")
pred_svc = svc_model.predict(texts)
pred_logistic = logistic_model.predict(texts)

# 5. The Ensemble Logic (OR Gate logic for maximum safety)
# Risk Hierarchy: Predatory > Caution > Safe
# If either model detects high risk, the Ensemble adopts the higher risk to protect the user.
ensemble_predictions = []
for s_vote, l_vote in zip(pred_svc, pred_logistic):
    if s_vote == "Predatory" or l_vote == "Predatory":
        ensemble_predictions.append("Predatory")
    elif s_vote == "Caution" or l_vote == "Caution":
        ensemble_predictions.append("Caution")
    else:
        ensemble_predictions.append("Safe")

# 6. Grade the Accuracy
acc_svc = accuracy_score(true_labels, pred_svc)
acc_logistic = accuracy_score(true_labels, pred_logistic)
acc_ensemble = accuracy_score(true_labels, ensemble_predictions)

# 7. Print the Pitch Deck Results
print("\n" + "="*50)
print("🏆 CLAUSEGUARD AI FACE-OFF RESULTS 🏆")
print("="*50)
print(f"🧠 Linear SVC Accuracy:         {acc_svc * 100:.1f}%")
print(f"🧠 Logistic Regression Accuracy: {acc_logistic * 100:.1f}%")
print("-" * 50)
print(f"🚀 COMBINED ENSEMBLE ACCURACY:   {acc_ensemble * 100:.1f}%")
print("="*50)

print("\n💡 Pitch Deck Idea: Tell the judges you used a 'Multi-Model Voting Ensemble'")
print("to guarantee maximum protection against predatory clauses!")