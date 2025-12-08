import requests
import random

# URL da sua API FastAPI (certifique-se que a porta está correta)
API_URL = "http://127.0.0.1:8000/predict"

def extrair_features_da_imagem(caminho_imagem):
    """
    IMPORTANTE: O modelo Random Forest treinado (breast_cancer_model.pkl) 
    espera 30 características numéricas (ex: raio médio, textura, etc), 
    e não uma imagem bruta (pixels).
    
    Em um cenário real, você usaria OpenCV ou Scikit-Image aqui para processar 
    a imagem e extrair essas medidas matemáticas.
    
    Como não temos esse extrator implementado, vamos simular os dados 
    para validar a conexão entre Django e FastAPI.
    """
    
    # Simulando dados válidos para o Pydantic do FastAPI aceitar
    # Se você tiver o extrator real, substitua este dicionário.
    return {
        "mean_radius": random.uniform(10, 20),
        "mean_texture": random.uniform(10, 25),
        "mean_perimeter": random.uniform(50, 150),
        "mean_area": random.uniform(300, 1000),
        "mean_smoothness": random.uniform(0.05, 0.15),
        "mean_compactness": random.uniform(0.05, 0.3),
        "mean_concavity": random.uniform(0, 0.4),
        "mean_concave_points": random.uniform(0, 0.2),
        "mean_symmetry": random.uniform(0.1, 0.3),
        "mean_fractal_dimension": random.uniform(0.05, 0.1),
        "radius_error": random.uniform(0, 1),
        "texture_error": random.uniform(0, 2),
        "perimeter_error": random.uniform(0, 10),
        "area_error": random.uniform(0, 100),
        "smoothness_error": random.uniform(0, 0.01),
        "compactness_error": random.uniform(0, 0.05),
        "concavity_error": random.uniform(0, 0.05),
        "concave_points_error": random.uniform(0, 0.02),
        "symmetry_error": random.uniform(0, 0.05),
        "fractal_dimension_error": random.uniform(0, 0.01),
        "worst_radius": random.uniform(10, 30),
        "worst_texture": random.uniform(15, 40),
        "worst_perimeter": random.uniform(60, 200),
        "worst_area": random.uniform(400, 2000),
        "worst_smoothness": random.uniform(0.08, 0.2),
        "worst_compactness": random.uniform(0.1, 0.6),
        "worst_concavity": random.uniform(0, 0.7),
        "worst_concave_points": random.uniform(0, 0.3),
        "worst_symmetry": random.uniform(0.2, 0.5),
        "worst_fractal_dimension": random.uniform(0.05, 0.15)
    }

def obter_predicao_api(caminho_imagem):
    """Envia os dados para a API FastAPI e retorna a resposta."""
    try:
        # 1. Extrair (ou simular) features
        dados_features = extrair_features_da_imagem(caminho_imagem)
        
        # 2. Enviar POST para o FastAPI
        response = requests.post(API_URL, json=dados_features)
        
        # 3. Verificar sucesso
        if response.status_code == 200:
            return response.json() # Retorna dict: {'predicted_class': '...', 'confidence': ...}
        else:
            print(f"Erro na API: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("Não foi possível conectar à API Backend. Verifique se ela está rodando.")
        return None