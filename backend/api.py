import os
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from .model_util import load_model, predict_instance

# 1. Configuração da Aplicação FastAPI
app = FastAPI(title="Breast Cancer API - Decision Tree")

# 2. Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Carregamento do Modelo de Machine Learning
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "breast_cancer_model.pkl")
model = load_model(MODEL_PATH)

# 4. Definição do Schema de Entrada (Payload)
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

# 5. Definição do Schema de Saída (Response)
class PredictionResponse(BaseModel):
    predicted_class: str
    confidence: float
    probabilities: List[float]

# 6. Endpoint Raiz (Verificação de Status)
@app.get("/")
def read_root():
    """Endpoint simples para verificar se a API está online."""
    return {
        "status": "API Online",
        "model": "Decision Tree",
        "version": "2.0"
    }

# 7. Endpoint Principal de Predição
@app.post("/predict", response_model=PredictionResponse)
def predict(data: BreastCancerInput):
    """
    Recebe os dados do tumor e retorna a predição de malignidade/benignidade.
    
    Args:
        data (BreastCancerInput): O corpo da requisição POST validado pelo Pydantic.
    """
    
    # 7.1. Extração e Organização dos Dados
    x = [
        data.mean_radius, data.mean_texture, data.mean_perimeter, data.mean_area, data.mean_smoothness,
        data.mean_compactness, data.mean_concavity, data.mean_concave_points, data.mean_symmetry, data.mean_fractal_dimension,
        data.radius_error, data.texture_error, data.perimeter_error, data.area_error, data.smoothness_error,
        data.compactness_error, data.concavity_error, data.concave_points_error, data.symmetry_error, data.fractal_dimension_error,
        data.worst_radius, data.worst_texture, data.worst_perimeter, data.worst_area, data.worst_smoothness,
        data.worst_compactness, data.worst_concavity, data.worst_concave_points, data.worst_symmetry, data.worst_fractal_dimension
    ]
    
    # 7.2. Execução da Predição
    pred_class, confidence, probs = predict_instance(model, x)
    
    # 7.3. Formatação da Resposta
    return PredictionResponse(
        predicted_class=pred_class,
        confidence=round(confidence, 4),
        probabilities=[round(float(p), 4) for p in probs.tolist()]
    )