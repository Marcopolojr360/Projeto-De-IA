import os, pickle
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "backend", "model")
os.makedirs(MODEL_DIR, exist_ok=True)

data = load_breast_cancer()
clf = RandomForestClassifier(n_estimators=10)
clf.fit(data.data, data.target)

with open(os.path.join(MODEL_DIR, "breast_cancer_model.pkl"), "wb") as f:
    pickle.dump(clf, f)
print("Modelo criado com sucesso!")