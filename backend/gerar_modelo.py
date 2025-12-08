import os
import pickle
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "breast_cancer_model.pkl")

os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

print(f"Gerando modelo em: {MODEL_PATH}")
data = load_breast_cancer()
clf = RandomForestClassifier(n_estimators=10, random_state=42)
clf.fit(data.data, data.target)

with open(MODEL_PATH, "wb") as f:
    pickle.dump(clf, f)
print("Sucesso!")