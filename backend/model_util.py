import os
import pickle
import numpy as np

def load_model(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"MODELO NAO ENCONTRADO EM: {path}")
    with open(path, "rb") as f:
        model = pickle.load(f)
    return model

def predict_instance(model, x):
    arr = np.array(x, dtype=float).reshape(1, -1)
    probs = model.predict_proba(arr)[0]
    idx = int(probs.argmax())
    confidence = float(probs[idx])
    classmap = {0: "Maligno", 1: "Benigno"}
    try:
        if hasattr(model, "classes"):
            label = model.classes_[idx]
            pred_name = classmap.get(int(label), str(label))
        else:
            pred_name = classmap.get(idx, str(idx))
    except:
        pred_name = str(idx)
    return pred_name, confidence, probs