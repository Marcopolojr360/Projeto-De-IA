import os  # Módulo para interação com o sistema operacional (caminhos de arquivo)
from fastapi import FastAPI # Importa a classe principal do framework FastAPI
from pydantic import BaseModel, Field # Importa classes para validação de dados (schema)
from typing import List # Usado para definir que um tipo é uma lista
from fastapi.middleware.cors import CORSMiddleware # Middleware para configurar CORS
from .model_util import load_model, predict_instance # Importa as funções de carregamento e predição

# 1. Configuração da Aplicação FastAPI
app = FastAPI(title="Breast Cancer API") # Cria a instância da aplicação com um título

# 2. Configuração do CORS (Cross-Origin Resource Sharing)
# Permite que aplicações frontend (como a sua interface de upload) rodando em 
# domínios diferentes possam se comunicar com esta API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite requisições de qualquer origem (em produção, defina domínios específicos)
    allow_credentials=True, # Permite cookies, cabeçalhos de autorização, etc.
    allow_methods=["*"], # Permite todos os métodos HTTP (GET, POST, etc.)
    allow_headers=["*"], # Permite todos os cabeçalhos HTTP
)

# 3. Carregamento do Modelo de Machine Learning
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Obtém o diretório base do arquivo atual
MODEL_PATH = os.path.join(BASE_DIR, "model", "breast_cancer_model.pkl") # Define o caminho completo do modelo serializado
model = load_model(MODEL_PATH) # Carrega o modelo usando a função importada

# 4. Definição do Schema de Entrada (Payload)
# Usa Pydantic (integrado ao FastAPI) para validar os dados de entrada JSON
class BreastCancerInput(BaseModel):
    # O modelo espera 30 características, cada uma com validação mínima (ge=0, Greater or Equal to 0)
    # Estas características correspondem às medidas das células de mama (raio, textura, área, etc.)
    mean_radius: float = Field(..., ge=0)
    mean_texture: float = Field(..., ge=0)
    mean_perimeter: float = Field(..., ge=0)
    mean_area: float = Field(..., ge=0)
    mean_smoothness: float = Field(..., ge=0)
    mean_compactness: float = Field(..., ge=0)
    mean_concavity: float = Field(..., ge=0)
    mean_concave_points: float = Field(..., ge=0)
    mean_symmetry: float = Field(..., ge=0)
    mean_fractal_dimension: float = Field(..., ge=0)
    radius_error: float = Field(..., ge=0)
    texture_error: float = Field(..., ge=0)
    perimeter_error: float = Field(..., ge=0)
    area_error: float = Field(..., ge=0)
    smoothness_error: float = Field(..., ge=0)
    compactness_error: float = Field(..., ge=0)
    concavity_error: float = Field(..., ge=0)
    concave_points_error: float = Field(..., ge=0)
    symmetry_error: float = Field(..., ge=0)
    fractal_dimension_error: float = Field(..., ge=0)
    worst_radius: float = Field(..., ge=0)
    worst_texture: float = Field(..., ge=0)
    worst_perimeter: float = Field(..., ge=0)
    worst_area: float = Field(..., ge=0)
    worst_smoothness: float = Field(..., ge=0)
    worst_compactness: float = Field(..., ge=0)
    worst_concavity: float = Field(..., ge=0)
    worst_concave_points: float = Field(..., ge=0)
    worst_symmetry: float = Field(..., ge=0)
    worst_fractal_dimension: float = Field(..., ge=0)

# 5. Definição do Schema de Saída (Response)
class PredictionResponse(BaseModel):
    # O que a API retornará após a predição
    predicted_class: str # Ex: "Maligno" ou "Benigno"
    confidence: float # Confiança da predição (probabilidade da classe escolhida)
    probabilities: List[float] # Lista de probabilidades para todas as classes

# 6. Endpoint Raiz (Verificação de Status)
@app.get("/")
def read_root():
    """Endpoint simples para verificar se a API está online."""
    return {"status": "API Online (Dentro de Cancer_de_mama)"}

# 7. Endpoint Principal de Predição
@app.post("/predict", response_model=PredictionResponse)
def predict(data: BreastCancerInput):
    """
    Recebe os dados do tumor e retorna a predição de malignidade/benignidade.
    
    Args:
        data (BreastCancerInput): O corpo da requisição POST validado pelo Pydantic.
    """
    
    # 7.1. Extração e Organização dos Dados
    # Converte o objeto Pydantic de entrada em uma lista Python simples
    # (É crucial manter a ordem correta das 30 características)
    x = [
        data.mean_radius, data.mean_texture, data.mean_perimeter, data.mean_area, data.mean_smoothness,
        data.mean_compactness, data.mean_concavity, data.mean_concave_points, data.mean_symmetry, data.mean_fractal_dimension,
        data.radius_error, data.texture_error, data.perimeter_error, data.area_error, data.smoothness_error,
        data.compactness_error, data.concavity_error, data.concave_points_error, data.symmetry_error, data.fractal_dimension_error,
        data.worst_radius, data.worst_texture, data.worst_perimeter, data.worst_area, data.worst_smoothness,
        data.worst_compactness, data.worst_concavity, data.worst_concave_points, data.worst_symmetry, data.worst_fractal_dimension
    ]
    
    # 7.2. Execução da Predição
    # Chama a função de predição do script utilitário
    pred_class, confidence, probs = predict_instance(model, x)
    
    # 7.3. Formatação da Resposta
    # Cria a resposta seguindo o schema PredictionResponse, arredondando os valores
    return PredictionResponse(
        predicted_class=pred_class,
        confidence=round(confidence, 4), # Arredonda a confiança para 4 casas decimais
        # Converte o array numpy de probabilidades para lista e arredonda os valores
        probabilities=[round(float(p), 4) for p in probs.tolist()]
    )