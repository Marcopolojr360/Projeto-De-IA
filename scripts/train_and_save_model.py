import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle
import os

def train_and_save():
    # 1. Definir caminhos baseados na localização deste script
    # O script está em: Projeto-De-IA/scripts/
    # Queremos salvar em: Projeto-De-IA/backend/model/
    
    current_dir = os.path.dirname(os.path.abspath(__file__)) # .../scripts
    base_dir = os.path.dirname(current_dir) # .../Projeto-De-IA
    
    # Define a pasta de destino no backend
    model_dir = os.path.join(base_dir, "backend", "model")
    os.makedirs(model_dir, exist_ok=True) # Cria a pasta se não existir
    
    output_path = os.path.join(model_dir, "breast_cancer_model.pkl")
    csv_path = os.path.join(current_dir, "data.csv") # Assume que o csv está na pasta scripts
    
    # Verifica se o CSV existe
    if not os.path.exists(csv_path):
        print(f"Erro: O arquivo de dados não foi encontrado em: {csv_path}")
        return

    print(f"Lendo dados de: {csv_path}")
    df = pd.read_csv(csv_path)

    # Pré-processamento
    if 'id' in df.columns:
        df = df.drop('id', axis=1)
    
    df = df.dropna(axis=1, how='all')

    y_raw = df['diagnosis']
    X = df.drop('diagnosis', axis=1)

    # Converter labels (M/B -> 1/0)
    le = LabelEncoder()
    y = le.fit_transform(y_raw)
    
    # Treinar Modelo
    print("Treinando modelo Random Forest...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Preparar objeto para salvar (Modelo + Classes)
    data_to_save = {
        "model": model,
        "classes": le.classes_ # Salva ['B', 'M'] para usar depois
    }

    # Salvar no backend
    with open(output_path, "wb") as f:
        pickle.dump(data_to_save, f)
    
    print(f"Sucesso! Modelo salvo em: {output_path}")

if __name__ == "__main__":
    train_and_save()