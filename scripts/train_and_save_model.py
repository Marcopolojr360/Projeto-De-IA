import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import pickle
import os

def train_and_save():
    # 1. Definir caminhos baseados na localização deste script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(current_dir)
    
    model_dir = os.path.join(base_dir, "backend", "model")
    os.makedirs(model_dir, exist_ok=True)
    
    output_path = os.path.join(model_dir, "breast_cancer_model.pkl")
    csv_path = os.path.join(current_dir, "data.csv")
    
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
    
    # Treinar Modelo Decision Tree
    print("Treinando modelo Decision Tree...")
    model = DecisionTreeClassifier(
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42
    )
    model.fit(X, y)
    
    # Calcular acurácia no conjunto de treinamento
    accuracy = model.score(X, y)
    print(f"Acurácia no conjunto de treinamento: {accuracy * 100:.2f}%")
    
    # Preparar objeto para salvar (Modelo + Classes)
    data_to_save = {
        "model": model,
        "classes": le.classes_
    }

    # Salvar no backend
    with open(output_path, "wb") as f:
        pickle.dump(data_to_save, f)
    
    print(f"Sucesso! Modelo salvo em: {output_path}")

if __name__ == "__main__":
    train_and_save()