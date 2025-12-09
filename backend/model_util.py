import os
import pickle
import numpy as np

def load_model(path: str):
    """
    Carrega o ficheiro binário (.pkl) do disco.
    """
    # Verifica se o ficheiro existe para evitar erros crípticos depois
    if not os.path.exists(path):
        raise FileNotFoundError(f"MODELO NAO ENCONTRADO EM: {path}")
    # Abre o ficheiro em modo de leitura binária (rb)
    with open(path, "rb") as f:
        data = pickle.load(f)
    # Retorna o dicionário contendo o modelo   
    return data 

def predict_instance(loaded_data, x):
   
    # 1. Conversão para NumPy
    # O Scikit-Learn espera um array 2D (matriz), mesmo para um único exemplo.
    # reshape(1, -1) transforma a lista [1, 2, 3] em [[1, 2, 3]].

    arr = np.array(x, dtype=float).reshape(1, -1)
    
    # Extração do Modelo
    model = None
    
   # Verifica se o ficheiro carregado é um dicionário novo (com metadados) ou antigo
    if isinstance(loaded_data, dict):
        model = loaded_data.get("model")
        scaler = loaded_data.get("scaler")
        classes = loaded_data.get("classes", ["B", "M"]) # Fallback
        
        # --- PASSO CRÍTICO: Aplicar a normalização ---
        # Se o modelo foi treinado com dados normalizados (média 0, desvio 1),
        # precisamos aplicar a MESMA transformação matemática aos dados novos.
        if scaler:
            arr = scaler.transform(arr)
    else:
        # Suporte legado (caso carregue um modelo antigo só com o objeto)
        model = loaded_data
        classes = ["B", "M"]

    # 3. Predição
    probs = model.predict_proba(arr)[0]
    # Descobre qual índice tem a maior probabilidade (0 ou 1)
    idx = int(probs.argmax())
    confidence = float(probs[idx])
    
    # Mapeamento
    classmap = {0: "Maligno", 1: "Benigno"}
    
    # Tradução do Resultado (De números para Português)
    # Usa as classes originais salvas no treino (ex: 'M', 'B')
    try:
        label = classes[idx]
        # Se label for 'M' (Maligno) ou 'B' (Benigno)
        if label == 'M': pred_name = "Maligno"
        elif label == 'B': pred_name = "Benigno"
        else: pred_name = str(label)
    except:
        pred_name = classmap.get(idx, str(idx))
        
    return pred_name, confidence, probs