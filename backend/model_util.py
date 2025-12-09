import os
import pickle
import numpy as np

def load_model(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"MODELO NAO ENCONTRADO EM: {path}")
    with open(path, "rb") as f:
        data = pickle.load(f)
    return data # Retorna o dicionário completo {'model': ..., 'scaler': ...}

def predict_instance(loaded_data, x):
    """
    Args:
        loaded_data: O dicionário carregado do pickle (contendo model e scaler)
        x: Lista de features
    """
    # 1. Preparação dos dados
    arr = np.array(x, dtype=float).reshape(1, -1)
    
    # 2. Extração do Modelo e Scaler
    model = None
    
    # Verifica se é o novo formato com Scaler
    if isinstance(loaded_data, dict):
        model = loaded_data.get("model")
        scaler = loaded_data.get("scaler")
        classes = loaded_data.get("classes", ["B", "M"]) # Fallback
        
        # --- PASSO CRÍTICO: Aplicar a normalização ---
        if scaler:
            arr = scaler.transform(arr)
    else:
        # Suporte legado (caso carregue um modelo antigo só com o objeto)
        model = loaded_data
        classes = ["B", "M"]

    # 3. Predição
    probs = model.predict_proba(arr)[0]
    idx = int(probs.argmax())
    confidence = float(probs[idx])
    
    # 4. Mapeamento
    classmap = {0: "Maligno", 1: "Benigno"}
    
    # Tenta usar as classes salvas no LabelEncoder
    try:
        label = classes[idx]
        # Se label for 'M' (Maligno) ou 'B' (Benigno)
        if label == 'M': pred_name = "Maligno"
        elif label == 'B': pred_name = "Benigno"
        else: pred_name = str(label)
    except:
        pred_name = classmap.get(idx, str(idx))
        
    return pred_name, confidence, probs