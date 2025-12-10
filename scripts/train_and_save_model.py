import pandas as pd
import pickle
import os
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

def train_and_save():
    # 1. Configuração de caminho
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(current_dir) 
    
    # Define onde salvar o modelo (pasta 'backend/model')
    model_dir = os.path.join(base_dir, "backend", "model")
    
    # Caminho do CSV
    csv_path = os.path.join(current_dir, "data.csv")
    output_path = os.path.join(model_dir, "breast_cancer_model.pkl")

    # Cria a pasta do modelo se não existir
    os.makedirs(model_dir, exist_ok=True)

    # 2. Carregamento dos Dados
    if not os.path.exists(csv_path):
        print(f"Arquivo não encontrado em: {csv_path}")
        return

    df = pd.read_csv(csv_path)

    # Limpeza básica
    if 'id' in df.columns:
        df = df.drop('id', axis=1)
    df = df.dropna(axis=1, how='all')

    # 3. Separação entre Dados de Entrada e Diagnóstico
    y_raw = df['diagnosis']
    X = df.drop('diagnosis', axis=1)

    le = LabelEncoder()
    y = le.fit_transform(y_raw)

    # 4. Divisão em Conjuntos de Treino e Teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # 5. Normalização
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # 6. Treinamento
    model = DecisionTreeClassifier(
        max_depth=5,
        min_samples_split=10,
        min_samples_leaf=5,
        random_state=42
    )
    model.fit(X_train, y_train)

    # 7. Validação
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    # 8. Empacotamento
    dataset_package = {
        "model": model,
        "classes": le.classes_,
        "scaler": scaler
    }

    with open(output_path, "wb") as f:
        pickle.dump(dataset_package, f)
    print("")
    print(f"Sucesso! Modelo salvo em: {output_path}")
    print("")
if __name__ == "__main__":
    train_and_save()