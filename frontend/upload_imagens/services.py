import os
import numpy as np
import random
import hashlib
import requests # Biblioteca para fazer a conexão HTTP com o backend

# URL da API do Backend (FastAPI)
# Certifique-se de que o backend esteja rodando nesta porta
API_URL = "http://127.0.0.1:8000/predict"

def extrair_features_da_imagem(caminho_imagem):
    """
    Simula a extração das 30 features.
    Gera dados brutos (sem normalização), pois o Backend cuidará do Scaler.
    """
    nome_arquivo = os.path.basename(caminho_imagem).lower()
    
    # 1. Seed baseada no hash da imagem para consistência
    try:
        with open(caminho_imagem, "rb") as f:
            conteudo_imagem = f.read()
            hash_imagem = hashlib.md5(conteudo_imagem).hexdigest()
            seed_val = int(hash_imagem, 16) % (2**32)
    except Exception as e:
        print(f"Erro ao ler imagem: {e}")
        seed_val = 42
    
    rng = random.Random(seed_val)

    # 2. Heurística (Maligno vs Benigno) baseada no nome
    if any(x in nome_arquivo for x in ['maligno', 'cancer', 'tumor', 'positivo']):
        eh_maligno = True
    elif any(x in nome_arquivo for x in ['saudavel', 'benigno', 'normal', 'negativo']):
        eh_maligno = False
    else:
        eh_maligno = rng.choice([True, False])

    features = []
    
    # 3. Geração de dados (Valores brutos)
    if eh_maligno:
        radius = rng.uniform(15, 25)
        texture = rng.uniform(20, 35)
        perimeter = rng.uniform(100, 180)
        area = rng.uniform(800, 2000)
        smoothness = rng.uniform(0.10, 0.14)
    else:
        radius = rng.uniform(6, 14)
        texture = rng.uniform(10, 20)
        perimeter = rng.uniform(40, 90)
        area = rng.uniform(200, 600)
        smoothness = rng.uniform(0.05, 0.09)

    features.extend([radius, texture, perimeter, area, smoothness])
    
    # Preenche o restante
    for _ in range(25):
        features.append(rng.uniform(0, 1))

    return np.array(features).reshape(1, -1)

def obter_predicao_api(caminho_imagem):
    """
    Função que conecta o Frontend ao Backend via HTTP.
    """
    try:
        # 1. Extrair features da imagem (simulado)
        features_array = extrair_features_da_imagem(caminho_imagem)
        features_list = features_array[0].tolist()

        # 2. Mapear as features para os nomes esperados pela API
        # A ordem deve ser rigorosamente a mesma usada no treinamento e na API
        colunas = [
            "mean_radius", "mean_texture", "mean_perimeter", "mean_area", "mean_smoothness",
            "mean_compactness", "mean_concavity", "mean_concave_points", "mean_symmetry", "mean_fractal_dimension",
            "radius_error", "texture_error", "perimeter_error", "area_error", "smoothness_error",
            "compactness_error", "concavity_error", "concave_points_error", "symmetry_error", "fractal_dimension_error",
            "worst_radius", "worst_texture", "worst_perimeter", "worst_area", "worst_smoothness",
            "worst_compactness", "worst_concavity", "worst_concave_points", "worst_symmetry", "worst_fractal_dimension"
        ]
        
        # Cria o dicionário JSON payload
        payload = dict(zip(colunas, features_list))

        # 3. Enviar requisição POST para o Backend
        print(f"Enviando requisição para: {API_URL}")
        response = requests.post(API_URL, json=payload)
        
        # 4. Processar resposta
        if response.status_code == 200:
            dados = response.json()
            # Retorna no formato que a view espera
            return {
                'predicted_class': dados.get('predicted_class', 'Desconhecido'),
                'confidence': dados.get('confidence', 0.0)
            }
        else:
            print(f"Erro na API: {response.status_code} - {response.text}")
            return {'predicted_class': 'Erro API', 'confidence': 0.0}

    except requests.exceptions.ConnectionError:
        print("Erro: Não foi possível conectar ao Backend. Verifique se ele está rodando.")
        return {'predicted_class': 'Backend Offline', 'confidence': 0.0}
        
    except Exception as e:
        print(f"Erro interno no serviço: {e}")
        return {'predicted_class': 'Erro Processamento', 'confidence': 0.0}