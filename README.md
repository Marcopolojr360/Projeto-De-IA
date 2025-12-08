# Projeto-De-IA
Trabalho de IA
# 🩺 Backend - Detecção de Câncer de Mama (IA)

(fazer uma descricao)

Siga este guia passo a passo para rodar o projeto no seu computador.

-----

## 🚀 1. Instalar o Python (Se não tiver)

O primeiro passo é garantir que o Python esteja instalado corretamente.

### 🪟 Windows

1.  Acesse [python.org/downloads](https://www.python.org/downloads/).
2.  Baixe a versão mais recente (botão amarelo).
3.  **MUITO IMPORTANTE:** Ao abrir o instalador, marque a caixinha **"Add Python to PATH"** antes de clicar em Install.
4.  Conclua a instalação.

### 🐧 Linux (Ubuntu/Debian)

Abra o seu terminal e rode os seguintes comandos (copie e cole):

```bash
sudo apt update
sudo apt install -y python3-full python3-pip
```

*(Digite sua senha de usuário se pedir e dê Enter).*

-----

## 📂 2. Preparar o Ambiente

Abra o terminal (Linux) ou Prompt de Comando/PowerShell (Windows) **dentro da pasta deste projeto**.

### Passo 2.1: Criar o Ambiente Virtual

Isso cria uma "caixa isolada" para não bagunçar seu computador.

  * **🪟 Windows:**

    ```powershell
    python -m venv .venv
    ```

  * **🐧 Linux:**

    ```bash
    python3 -m venv .venv
    ```

### Passo 2.2: Ativar o Ambiente

Você precisa "entrar" nessa caixa isolada.

  * **🪟 Windows:**

    ```powershell
    .\.venv\Scripts\activate
    ```

    *(Se der erro de permissão, rode `Set-ExecutionPolicy Unrestricted -Scope Process` e tente de novo).*

  * **🐧 Linux:**

    ```bash
    source .venv/bin/activate
    ```

✅ **Como saber se funcionou?** O seu terminal deve mostrar `(.venv)` no começo da linha.

-----

## 📦 3. Instalar Dependências

Com o `(.venv)` aparecendo no terminal, instale as ferramentas necessárias:

```bash
pip install fastapi uvicorn scikit-learn pandas numpy pydantic
```

-----

## 🧠 4. Gerar o Modelo de IA

Antes de iniciar o servidor, precisamos "treinar" e salvar o arquivo de inteligência artificial. Existe um script pronto para isso.

No terminal (ainda com o `.venv` ativo), rode:

  * **🪟 Windows:**

    ```powershell
    python gerar_modelo.py
    ```

  * **🐧 Linux:**

    ```bash
    python3 gerar_modelo.py
    ```

✅ Se aparecer **"Sucesso\!"**, o arquivo foi criado.

-----

## ▶️ 5. Rodar o Servidor (Backend)

Agora vamos colocar a API no ar.

Execute o comando:

```bash
uvicorn Cancer_de_mama.backend.api:app --reload
```

Se tudo der certo, você verá uma mensagem verde parecida com esta:

> `INFO: Uvicorn running on http://127.0.0.1:8000`

-----

## 🧪 Como Testar?

1.  Não feche o terminal onde o servidor está rodando.
2.  Abra seu navegador (Chrome, Firefox, etc).
3.  Acesse o link: **[http://127.0.0.1:8000/docs](https://www.google.com/search?q=http://127.0.0.1:8000/docs)**
4.  Você verá uma tela azul (Swagger UI).
5.  Clique em **POST /predict** \> **Try it out** \> **Execute**.
6.  Se aparecer **Code 200** e uma resposta com "Maligno" ou "Benigno", seu backend está perfeito\!

## 👤 Equipe
- Marcos
- Renato
- Raica
- Victor
- Predo
- Nicolas 