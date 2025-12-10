# Importação das ferramentas necessárias
import pandas as pd  # Para ler e mexer na tabela de dados (CSV)
import pickle        # Para salvar o "cérebro" da IA num ficheiro .pkl
import os            # Para lidar com pastas e caminhos do sistema
from sklearn.tree import DecisionTreeClassifier       # O modelo de IA (Árvore de Decisão)
from sklearn.preprocessing import LabelEncoder, StandardScaler # Ferramentas de tradução e ajuste de escala
from sklearn.model_selection import train_test_split  # A FERRAMENTA DE DIVISÃO QUE FALÁMOS
from sklearn.metrics import accuracy_score, classification_report

def train_and_save():
 
    # Descobre onde este script está no computador para não haver erros de "ficheiro não encontrado"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(current_dir) 
    
    # Define onde o modelo final será guardado: pasta 'backend/model'
    model_dir = os.path.join(base_dir, "backend", "model")
    
    # Localiza o ficheiro com os dados dos pacientes (data.csv)
    csv_path = os.path.join(current_dir, "data.csv")
    output_path = os.path.join(model_dir, "breast_cancer_model.pkl")

    # Cria a pasta se ela não existir
    os.makedirs(model_dir, exist_ok=True)


    if not os.path.exists(csv_path):
        print(f"Arquivo não encontrado em: {csv_path}")
        return

    # Lê a tabela de dados
    df = pd.read_csv(csv_path)

    # Joga fora a coluna 'id' (o número do paciente não causa cancro)
    if 'id' in df.columns:
        df = df.drop('id', axis=1)
    
    # Limpa linhas que estejam completamente vazias
    df = df.dropna(axis=1, how='all')

  
    #A coluna com o diagnóstico original ('M' ou 'B')
    y_raw = df['diagnosis']
    
    #Todo o resto da tabela, exceto o diagnóstico (Raio, Textura, etc.)
    X = df.drop('diagnosis', axis=1)

    # Traduz 'M' e 'B' para números (1 e 0) para a IA entender
    le = LabelEncoder()
    y = le.fit_transform(y_raw)

   
    # Aqui separamos a "Escola" (Train) da "Prova" (Test).
    # X_train: Dados para estudar (80%)
    # X_test:  Dados para a prova (20%) - A IA nunca viu estes antes!
    # y_train: Gabarito de estudo
    # y_test:  Gabarito da prova
    # stratify=y: Garante que se temos 30% de casos Malignos no total,
    #             teremos 30% no treino e 30% no teste (não fica desequilibrado).
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

   
    # Faz com que "Área=1000" e "Suavidade=0.1" tenham o mesmo peso matemático.
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train) # Ajusta a régua com base no treino
    X_test = scaler.transform(X_test)       # Aplica a mesma régua no teste


    # Cria uma Árvore de Decisão com limites para não "decorar" demais (overfitting)
    model = DecisionTreeClassifier(
        max_depth=5,
        min_samples_split=10,
        min_samples_leaf=5,
        random_state=42
    )
    # A linha mágica: A IA analisa os padrões entre X_train e y_train
    model.fit(X_train, y_train)

   
    # Pede para a IA adivinhar os resultados do teste
    predictions = model.predict(X_test)
    
    # Compara o que ela adivinhou (predictions) com o gabarito real (y_test)
    accuracy = accuracy_score(y_test, predictions)

  
    # Guarda o modelo, a régua de normalização (scaler) e os nomes das classes
    dataset_package = {
        "model": model,
        "classes": le.classes_,
        "scaler": scaler
    }

    # Grava no disco como um arquivo .pkl
    with open(output_path, "wb") as f:
        pickle.dump(dataset_package, f)
        
    print("")
    print(f"Sucesso! Modelo salvo em: {output_path}")
    print("")

if __name__ == "__main__":
    train_and_save()