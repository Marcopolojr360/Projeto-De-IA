import os
import pickle
import numpy as np
import random
import hashlib
from django.conf import settings

# Ajuste do caminho:
# settings.BASE_DIR (diretório raiz do projeto Django - ex: Projeto-De-IA/frontend)
# Precisamos voltar uma pasta (..) e entrar em backend/model
MODEL_PATH = os.path.abspath(os.path.join(settings.BASE_DIR, '..', 'backend', 'model', 'breast_cancer_model.pkl'))

def carregar_modelo():
    """
    Carrega o modelo de Machine Learning serializado (.pkl) do disco.
    Esta função é crítica, pois carrega o objeto que faz a predição.
    """
    # 1. Verifica se o arquivo do modelo existe
    if not os.path.exists(MODEL_PATH):
        # Em caso de falha, imprime informações de debug e retorna None
        print(f"ERRO CRÍTICO: Modelo não encontrado.")
        print(f"O sistema buscou em: {MODEL_PATH}")
        return None, None
        
    # 2. Abre o arquivo em modo binário de leitura ('rb')
    with open(MODEL_PATH, "rb") as f:
        data = pickle.load(f)
        
    # 3. Tratamento de compatibilidade
    # Verifica se o modelo foi salvo como um dicionário (ex: {"model": objeto, "classes": [...]})
    if isinstance(data, dict) and "model" in data:
        return data["model"], data["classes"]
    else:
        # Assume que o objeto salvo é o próprio modelo e define as classes padrão
        return data, ["B", "M"] # B = Benigno, M = Maligno

def extrair_features_da_imagem(caminho_imagem):
    """
    Simula a extração das 30 features do WDBC (Wisconsin Diagnostic Breast Cancer)
    baseando-se no nome e conteúdo da imagem para manter a consistência.
    
    Esta função NÃO FAZ PROCESSAMENTO REAL DE IMAGEM, apenas gera dados realistas.
    """
    nome_arquivo = os.path.basename(caminho_imagem).lower()
    
    # 1. Geração de Seed Consistente
    # Usa o hash MD5 do conteúdo da imagem para garantir que a mesma imagem 
    # sempre gere os mesmos números aleatórios (predição consistente)
    try:
        with open(caminho_imagem, "rb") as f:
            conteudo_imagem = f.read()
            hash_imagem = hashlib.md5(conteudo_imagem).hexdigest()
            # Converte o hash para um inteiro para ser usado como seed
            seed_val = int(hash_imagem, 16) % (2**32)
    except Exception as e:
        print(f"Erro ao ler imagem: {e}")
        seed_val = 42
    
    rng = random.Random(seed_val)

    # 2. Heurística de Predição Baseada no Nome do Arquivo
    # Tenta determinar a intenção da simulação (Maligno ou Benigno)
    if any(x in nome_arquivo for x in ['maligno', 'cancer', 'tumor', 'positivo']):
        eh_maligno = True
    elif any(x in nome_arquivo for x in ['saudavel', 'benigno', 'normal', 'negativo']):
        eh_maligno = False
    else:
        # Caso o nome não seja sugestivo, decide aleatoriamente (mas de forma consistente)
        eh_maligno = rng.choice([True, False])

    features = []
    
    # 

[Image of the difference between benign and malignant cell structures]

    # 3. Geração de Dados Realista por Categoria (Maligno vs. Benigno)
    
    if eh_maligno:
        # Tumores malignos: células grandes, irregulares, alta área
        radius = rng.uniform(15, 25)      # Raio Grande
        texture = rng.uniform(20, 35)     # Textura Irregular/Alta
        perimeter = rng.uniform(100, 180) # Perímetro Grande
        area = rng.uniform(800, 2000)     # Área Grande
        smoothness = rng.uniform(0.10, 0.14)
    else:
        # Tumores benignos: células pequenas, lisas, baixa área
        radius = rng.uniform(6, 14)      # Raio Pequeno
        texture = rng.uniform(10, 20)    # Textura Baixa/Lisa
        perimeter = rng.uniform(40, 90)  # Perímetro Pequeno
        area = rng.uniform(200, 600)     # Área Pequena
        smoothness = rng.uniform(0.05, 0.09)

    # Adiciona as 5 primeiras features principais (que são as mais impactantes no modelo)
    features.extend([radius, texture, perimeter, area, smoothness])
    
    # Preenche o resto das 25 features com valores pequenos aleatórios para completar as 30
    for _ in range(25):
        features.append(rng.uniform(0, 1))

    # Retorna o array NumPy no formato (1, 30) esperado pelo modelo
    return np.array(features).reshape(1, -1)

# 4. Função Principal de Predição (Simulação de Chamada de API/Serviço)
def obter_predicao_api(caminho_imagem):
    """
    Função que executa a predição usando o modelo local.
    """
    try:
        model, classes = carregar_modelo()
        
        if model is None:
            return {'predicted_class': 'Erro: Modelo não encontrado', 'confidence': 0.0}

        # Extrai as features simuladas
        features_array = extrair_features_da_imagem(caminho_imagem)

        # 5. Validação de Dimensão
        if features_array.shape[1] != 30:
             # Ajuste para garantir que o array tenha exatamente 30 colunas
             features_array = np.resize(features_array, (1, 30))

        # 6. Predição
        # Obtém as probabilidades para cada classe
        probs = model.predict_proba(features_array)[0]
        prediction_idx = probs.argmax()
        confidence = probs[prediction_idx]
        
        # 7. Mapeamento de Resultado
        # Mapeia o índice do modelo (0 ou 1) para o nome da classe ('Benigno' ou 'Maligno')
        label_real = classes[prediction_idx]
        # A ordem no `classes` é geralmente ['B', 'M']. Se for 'M', é 0 (maligno); se 'B', é 1 (benigno).
        # Nota: O mapeamento `resultado_texto` aqui deve ser verificado com a ordem real das classes do modelo.
        # Assumindo que o índice 0 seja Benigno e 1 seja Maligno no `probs`:
        resultado_texto = "Benigno" if label_real == 'B' else "Maligno"


        return {
            'predicted_class': resultado_texto,
            'confidence': float(confidence)
        }

    except Exception as e:
        print(f"Erro na previsão local: {e}")
        import traceback
        traceback.print_exc()
        return {'predicted_class': 'Erro Processamento', 'confidence': 0.0}