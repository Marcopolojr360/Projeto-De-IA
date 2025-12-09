import os
import pickle
import numpy as np

def load_model(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"MODELO NAO ENCONTRADO EM: {path}")
    
    with open(path, "rb") as f:
        data = pickle.load(f)
    
    # IMPORTANTE: Verifica se é o dicionário antigo e extrai o modelo real
    if isinstance(data, dict) and "model" in data:
        return data["model"]
    
    return data

def predict_instance(model, x):
    # Garante que a entrada seja 2D (formato esperado pelo sklearn)
    arr = np.array(x, dtype=float).reshape(1, -1)
    
    # Faz a predição das probabilidades
    probs = model.predict_proba(arr)[0]
    
    # Pega o índice da maior probabilidade
    idx = int(probs.argmax())
    confidence = float(probs[idx])
    
    # Mapeamento correto: 0 = Benigno, 1 = Maligno (ordem alfabética do LabelEncoder)
    classmap = {0: "Benigno", 1: "Maligno"}
    
    # Define o nome da predição
    pred_name = classmap.get(idx, str(idx))
    
    return pred_name, confidence, probs