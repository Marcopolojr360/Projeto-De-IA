import os       # Módulo para interagir com o sistema operacional (verificação de arquivos)
import pickle   # Módulo usado para serializar e desserializar objetos Python (salvar/carregar modelos)
import numpy as np # Biblioteca fundamental para computação numérica e manipulação de arrays

def load_model(path: str):
    """
    Carrega um modelo de Machine Learning serializado usando pickle.

    Args:
        path (str): Caminho completo para o arquivo do modelo (.pkl).

    Returns:
        object: O objeto do modelo carregado.
        
    Raises:
        FileNotFoundError: Se o arquivo do modelo não existir no caminho especificado.
    """
    # 1. Verifica a existência do arquivo do modelo
    if not os.path.exists(path):
        # Se o arquivo não for encontrado, lança uma exceção
        raise FileNotFoundError(f"MODELO NAO ENCONTRADO EM: {path}")
        
    # 2. Abre o arquivo em modo de leitura binária ('rb')
    with open(path, "rb") as f:
        # 3. Desserializa o objeto do modelo do arquivo
        model = pickle.load(f)
        
    # 4. Retorna o modelo
    return model

def predict_instance(model, x):
    """
    Realiza a previsão em uma única instância (conjunto de características) 
    usando o modelo carregado e retorna o diagnóstico e a confiança.

    Args:
        model (object): O modelo de ML carregado (ex: LogisticRegression, SVC).
        x (list/array): Lista ou array contendo as características da instância a ser prevista.

    Returns:
        tuple: (pred_name, confidence, probs) onde:
               - pred_name (str): O nome da classe prevista ("Maligno" ou "Benigno").
               - confidence (float): A probabilidade (confiança) da classe prevista.
               - probs (np.array): O array de probabilidades para todas as classes.
    """
    
    # 1. Preparação dos dados de entrada
    # Converte a lista 'x' em um array NumPy, garante que seja do tipo float,
    # e remodela para o formato esperado pelo modelo (1 linha, N colunas)
    arr = np.array(x, dtype=float).reshape(1, -1)
    
    # 2. Obtenção das Probabilidades
    # Calcula as probabilidades de pertencer a cada classe. [0] pega o resultado 
    # para a primeira (e única) instância que estamos prevendo.
    probs = model.predict_proba(arr)[0]
    
    # 3. Determinação da Previsão de Maior Confiança
    # Encontra o índice da classe com a maior probabilidade
    idx = int(probs.argmax())
    
    # Pega o valor da probabilidade (confiança) do índice escolhido
    confidence = float(probs[idx])
    
    # 4. Mapeamento das Classes
    # Dicionário para traduzir o índice numérico da classe para um nome legível
    classmap = {0: "Maligno", 1: "Benigno"}
    
    # 5. Tentativa de Obter o Nome da Classe
    try:
        # Se o modelo tiver o atributo 'classes_' (comum em sklearn), usa o label real
        if hasattr(model, "classes"):
            label = model.classes_[idx]
            # Mapeia o label numérico para o nome usando o classmap
            pred_name = classmap.get(int(label), str(label))
        else:
            # Caso contrário, usa diretamente o índice (idx) para mapear
            pred_name = classmap.get(idx, str(idx))
    except:
        # Em caso de qualquer erro no mapeamento, usa o índice como nome
        pred_name = str(idx)
        
    # 6. Retorno dos Resultados
    return pred_name, confidence, probs