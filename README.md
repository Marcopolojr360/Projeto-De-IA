# Detecção de Câncer de Mama (IA)

Este projeto consiste em uma aplicação web completa (Fullstack) desenvolvida para auxiliar na detecção precoce de câncer de mama utilizando Inteligência Artificial.

A solução integra um **Frontend** interativo para envio de exames, um **Backend** e um modelo de **Machine Learning Supervisionado** (Random Forest) capaz de analisar padrões em dados médicos e classificar diagnósticos com alta precisão.

### 🛠️ Tecnologias Utilizadas
* **Frontend & Uploads:** Python (Django) - Gerenciamento de interface e arquivos de mídia.
* **Backend & API:** FastAPI - Processamento rápido das requisições.
* **Inteligência Artificial:** Scikit-Learn - Modelo supervisionado para classificação (Benigno/Maligno).
* **Banco de Dados:** SQLite (Padrão Django) para persistência de dados.

### 🎯 Objetivo
Facilitar a triagem de diagnósticos médicos através de uma interface simples onde profissionais ou pacientes podem enviar imagens/dados, recebendo uma predição instantânea baseada em aprendizado de máquina.

# 🖥️ Frontend - Interface Web (Django)

Este guia ajuda qualquer pessoa a rodar a parte visual (o site) do projeto de Detecção de Câncer de Mama. Esta aplicação foi feita utilizando **Python** e **Django**.

Siga os passos abaixo na ordem exata.

-----

## 🚀 1. Instalar o Python (Se não tiver)

Se você já instalou o Python para o backend, pode pular para o Passo 2. Caso contrário:

### 🪟 Windows

1.  Acesse [python.org/downloads](https://www.python.org/downloads/).
2.  Baixe a versão mais recente (botão amarelo).
3.  **MUITO IMPORTANTE:** Ao abrir o instalador, marque a opção **"Add Python to PATH"** na parte inferior da janela antes de clicar em *Install*.
4.  Conclua a instalação clicando em *Close*.

### 🐧 Linux (Ubuntu/Debian)

Abra o seu terminal (Ctrl+Alt+T) e rode os comandos abaixo:

```bash
sudo apt update
sudo apt install -y python3-full python3-pip
````

*(Digite sua senha de usuário se pedir e dê Enter. A senha não aparece enquanto você digita, isso é normal).*

-----

## 📂 2. Preparar o Ambiente

Abra o terminal (Linux) ou Prompt de Comando/PowerShell (Windows) **dentro da pasta deste projeto** (onde está o arquivo `manage.py`).

### Passo 2.1: Criar o Ambiente Virtual

Isso cria uma pasta isolada para instalar as bibliotecas do projeto sem interferir no seu sistema.

  * **🪟 Windows:**

    ```powershell
    python -m venv .venv_front
    ```

  * **🐧 Linux:**

    ```bash
    python3 -m venv .venv_front
    ```

### Passo 2.2: Ativar o Ambiente

Agora vamos "entrar" nessa pasta isolada.

  * **🪟 Windows:**

    ```powershell
    .\.venv_front\Scripts\activate
    ```

    *(Se aparecer um erro vermelho sobre scripts, rode: `Set-ExecutionPolicy Unrestricted -Scope Process` e tente ativar de novo).*

  * **🐧 Linux:**

    ```bash
    source .venv_front/bin/activate
    ```

✅ **Como saber se funcionou?** O seu terminal deve mostrar `(.venv_front)` no começo da linha.

-----

## 📦 3. Instalar Dependências (Django)

Com o `(.venv_front)` ativo no terminal, vamos instalar o **Django** e outras ferramentas necessárias para lidar com imagens e conexões.

Execute:

```bash
pip install django pillow requests
```

  * `django`: O framework principal do site.
  * `pillow`: Biblioteca para lidar com o upload de imagens (ex: mamografias).
  * `requests`: Útil caso o frontend precise conversar com o backend de IA.

-----

## 🛠️ 4. Configurar o Banco de Dados

O Django precisa criar um pequeno banco de dados local para funcionar. Basta rodar este comando:

  * **🪟 Windows:**

    ```powershell
    python manage.py migrate
    ```

  * **🐧 Linux:**

    ```bash
    python3 manage.py migrate
    ```

✅ Se aparecerem várias linhas com **OK** verde, deu certo.

-----

## ▶️ 5. Rodar o Site

Agora vamos colocar o site no ar\!

⚠️ **Atenção:** Se o seu Backend (API) já estiver rodando na porta 8000, o Django pode dar erro. Recomendo rodar o Django em uma porta diferente (ex: 8001).

No terminal (com o venv ativo), rode:

  * **🪟 Windows:**

    ```powershell
    python manage.py runserver 8001
    ```

  * **🐧 Linux:**

    ```bash
    python3 manage.py runserver 8001
    ```

Se tudo der certo, você verá algo como:

> `Starting development server at http://127.0.0.1:8001/`


## 🧪 Como Acessar?

1.  Mantenha o terminal aberto (se fechar, o site cai).
2.  Abra seu navegador.
3.  Acesse: **[http://127.0.0.1:8001](https://www.google.com/search?q=http://127.0.0.1:8001)**

Pronto\! A interface visual deve carregar.


## 📂 1. Preparar o Ambiente

Abra o terminal (Linux) ou Prompt de Comando/PowerShell (Windows) **dentro da pasta deste projeto**.

### Passo 1.1: Criar o Ambiente Virtual

Isso cria uma "caixa isolada" para não bagunçar seu computador.

  * **🪟 Windows:**

    ```powershell
    python -m venv .venv
    ```

  * **🐧 Linux:**

    ```bash
    python3 -m venv .venv
    ```

### Passo 1.2: Ativar o Ambiente

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

## 📦 2. Instalar Dependências

Com o `(.venv)` aparecendo no terminal, instale as ferramentas necessárias:

```bash
pip install fastapi uvicorn scikit-learn pandas numpy pydantic
```

-----

## 🧠 3. Gerar o Modelo de IA

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

## ▶️ 4. Rodar o Servidor (Backend)

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
- Marcos Paulo
- Nicolas do Vale
- Pedro Priori
- Raica Lyra
- Renato Nascimento
- Victor Gabriel