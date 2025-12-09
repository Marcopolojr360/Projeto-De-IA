import os
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from .model_util import load_model, predict_instance

# Cria a instância da aplicação FastAPI.
app = FastAPI(title="Breast Cancer API - Decision Tree")

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carregamento do Modelo de Machine Learning
# Define o caminho absoluto para o ficheiro .pkl onde o modelo treinado está guardado.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "breast_cancer_model.pkl")

# Carrega o modelo para a memória RAM assim que o servidor inicia.
# Isso evita ter que carregar o ficheiro a cada pedido, o que seria lento.
model = load_model(MODEL_PATH)

# Define EXATAMENTE o que o Frontend deve enviar.
# Se o Frontend enviar uma string onde deveria ser um float, ou esquecer um campo,
# o FastAPI rejeita o pedido automaticamente com um erro claro.
class BreastCancerInput(BaseModel):
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

# Define o formato da resposta que vamos enviar de volta.
class PredictionResponse(BaseModel):
    predicted_class: str
    confidence: float
    probabilities: List[float]

# Endpoint Raiz (Verificação de Status)
@app.get("/")
def read_root():
    """Endpoint simples para verificar se a API está online."""
    return {
        "status": "API Online",
        "model": "Decision Tree",
        "version": "2.0"
    }

# Recebe os dados, processa e devolve o diagnóstico.
@app.post("/predict", response_model=PredictionResponse)
def predict(data: BreastCancerInput):
    """
    Recebe os dados do tumor e retorna a predição de malignidade/benignidade.
    """
    
    # Extração e Organização dos Dados
    x = [
        data.mean_radius, data.mean_texture, data.mean_perimeter, data.mean_area, data.mean_smoothness,
        data.mean_compactness, data.mean_concavity, data.mean_concave_points, data.mean_symmetry, data.mean_fractal_dimension,
        data.radius_error, data.texture_error, data.perimeter_error, data.area_error, data.smoothness_error,
        data.compactness_error, data.concavity_error, data.concave_points_error, data.symmetry_error, data.fractal_dimension_error,
        data.worst_radius, data.worst_texture, data.worst_perimeter, data.worst_area, data.worst_smoothness,
        data.worst_compactness, data.worst_concavity, data.worst_concave_points, data.worst_symmetry, data.worst_fractal_dimension
    ]
    
    # Execução do diagnostico
    pred_class, confidence, probs = predict_instance(model, x)
    
    # Empacota os resultados no formato JSON esperado pelo Frontend
    return PredictionResponse(
        predicted_class=pred_class,
        confidence=round(confidence, 4),
        probabilities=[round(float(p), 4) for p in probs.tolist()]
    )