import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import pickle
import os

def train_and_save():

    # Descobre a pasta onde este script está salvo atualmente.
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Define a pasta pai (base) para poder navegar para outras pastas do projeto.
    base_dir = os.path.dirname(current_dir)
    
    # Cria o caminho para salvar o modelo final: backend/model/
    model_dir = os.path.join(base_dir, "backend", "model")

    # Cria a pasta se ela ainda não existir (evita erros).
    os.makedirs(model_dir, exist_ok=True)
    
    # Define o caminho completo onde o arquivo do modelo (.pkl) será salvo.
    output_path = os.path.join(model_dir, "breast_cancer_model.pkl")

    # Define o caminho onde o script espera encontrar o arquivo de dados (data.csv).
    csv_path = os.path.join(current_dir, "data.csv")
    
    # Verificação de segurança: se o CSV não existir, para o script.
    if not os.path.exists(csv_path):
        print(f"Erro: O arquivo de dados não foi encontrado em: {csv_path}")
        return

    print(f"Lendo dados de: {csv_path}")
    df = pd.read_csv(csv_path)

    # Remove a coluna 'id', pois é apenas um identificador e não ajuda a prever câncer.
    if 'id' in df.columns:
        df = df.drop('id', axis=1)
    
    # Remove colunas que estejam completamente vazias (NaN), se houverem.
    df = df.dropna(axis=1, how='all')

    # Separa o alvo (o que queremos prever: 'diagnosis') das características (medidas: 'radius', etc).  
    y_raw = df['diagnosis'] # Alvo
    X = df.drop('diagnosis', axis=1) # Features

    # O modelo matemático não entende letras ('M' ou 'B'). 
    # O LabelEncoder converte essas letras em números (ex: Maligno=1, Benigno=0).
    le = LabelEncoder()
    y = le.fit_transform(y_raw)
    
    # Treinar Modelo Decision Tree
    print("Treinando modelo Decision Tree...")
    # Cria a Árvore de Decisão com configurações específicas (hiperparâmetros)
    # para evitar que a árvore fique complexa demais (overfitting).
    model = DecisionTreeClassifier(
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42
    )
    # "Ensina" o modelo relacionando as medidas (X) com os diagnósticos (y).
    model.fit(X, y)
    
    # Verifica a taxa de acerto do modelo usando os próprios dados de treino.
    accuracy = model.score(X, y)
    print(f"Acurácia no conjunto de treinamento: {accuracy * 100:.2f}%")
    
    # Cria um pacote contendo o modelo treinado E o codificador de classes.
    # Isso é crucial para sabermos depois que 0=Benigno e 1=Maligno.
    data_to_save = {
        "model": model,
        "classes": le.classes_
    }

    # Salva esse pacote em um arquivo binário (.pkl) usando a biblioteca Pickle.
    with open(output_path, "wb") as f:
        pickle.dump(data_to_save, f)
    
    print(f"Sucesso! Modelo salvo em: {output_path}")

if __name__ == "__main__":
    train_and_save()