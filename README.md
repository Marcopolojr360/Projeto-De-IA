# 🩺 Detecção de Câncer de Mama (IA)

Este projeto consiste em uma aplicação web completa (Fullstack) desenvolvida para auxiliar na detecção precoce de câncer de mama utilizando Inteligência Artificial.

A solução integra um **Frontend** interativo para envio de exames, um **Backend** e um modelo de **Machine Learning Supervisionado** (Random Forest) capaz de analisar padrões em dados médicos e classificar diagnósticos com alta precisão.

## 🛠️ Tecnologias Utilizadas
* **Frontend & Uploads:** Python (Django) - Gerenciamento de interface e arquivos de mídia
* **Backend & API:** FastAPI - Processamento rápido das requisições
* **Inteligência Artificial:** Scikit-Learn - Modelo supervisionado para classificação (Benigno/Maligno)
* **Banco de Dados:** SQLite (Padrão Django) para persistência de dados

## 🎯 Objetivo
Facilitar a triagem de diagnósticos médicos através de uma interface simples onde profissionais ou pacientes podem enviar imagens/dados, recebendo uma predição instantânea baseada em aprendizado de máquina.


## 📋 Índice
1. [Instalar o Python](#1-instalar-o-python)
2. [Preparar o Backend (API)](#2-preparar-o-backend-api)
3. [Preparar o Frontend (Site)](#3-preparar-o-frontend-site)
4. [Rodar o Projeto](#4-rodar-o-projeto)
5. [Solução de Problemas](#5-solução-de-problemas)



## 1️⃣ Instalar o Python

### | Windows

1. Acesse [python.org/downloads](https://www.python.org/downloads/)
2. Baixe a versão mais recente (botão amarelo grande)
3. **⚠️ MUITO IMPORTANTE:** Ao abrir o instalador, marque a opção **"Add Python to PATH"** na parte inferior da janela ANTES de clicar em *Install Now*
4. Clique em *Install Now* e aguarde
5. Quando terminar, clique em *Close*

### Como verificar se instalou corretamente:
1. Aperte as teclas `Windows + R`
2. Digite `cmd` e aperte Enter
3. No terminal preto que abrir, digite: `python --version`
4. Se aparecer algo como `Python 3.12.x`, deu certo! ✅

### | Linux (Ubuntu/Debian)

### 1. Abra o terminal (aperte `Ctrl + Alt + T`)
### 2. Cole os comandos abaixo (um de cada vez) e aperte Enter:

```bash
sudo apt update
sudo apt install -y python3-full python3-pip
```

### 3. Digite sua senha de usuário quando pedir (a senha não aparece enquanto você digita, é normal)

### Como verificar se instalou corretamente:
Digite no terminal:
```bash
python3 --version
```
Se aparecer algo como `Python 3.12.x`, deu certo! ✅



## 2️⃣ Preparar o Backend (API)

O Backend é a parte que faz a inteligência artificial funcionar. Vamos configurá-lo primeiro.

## * Passo 1: Abrir o Terminal na Pasta Correta

### | Windows:
1. Abra a pasta do projeto no Windows Explorer
2. Clique com o botão direito em um espaço vazio dentro da pasta
3. Selecione **"Abrir no Terminal"** ou **"Abrir janela do PowerShell aqui"**

**OU:**

1. Abra o terminal (Windows + R, digite `cmd`, Enter)
2. Use o comando `cd` para navegar até a pasta. Exemplo:
```powershell
cd C:\Users\SeuNome\Downloads\Cancer_de_mama
```

### | Linux:
1. Abra o terminal (Ctrl + Alt + T)
2. Use o comando `cd` para navegar até a pasta. Exemplo:
```bash
cd ~/Downloads/Cancer_de_mama
```

**OU:**

1. Abra a pasta do projeto no gerenciador de arquivos
2. Clique com o botão direito e selecione **"Abrir no Terminal"**

## * Passo 2: Criar o Ambiente Virtual do Backend

Isso cria uma "caixa isolada" para não bagunçar seu computador.

### | Windows:
```powershell
python -m venv .venv_backend
```

### | Linux:
```bash
python3 -m venv .venv_backend
```

## * Passo 3: Ativar o Ambiente Virtual

Você precisa "entrar" nessa caixa isolada.

### | Windows:
```powershell
.\.venv_backend\Scripts\activate
```

**Se der erro de permissão**, rode este comando primeiro:
```powershell
Set-ExecutionPolicy Unrestricted -Scope Process
```
E depois tente ativar novamente.

### | Linux:
```bash
source .venv_backend/bin/activate
```

✅ **Como saber se funcionou?**  
O seu terminal deve mostrar `(.venv_backend)` no começo da linha, assim:
```
(.venv_backend) C:\Users\SeuNome\Cancer_de_mama>
```

## * Passo 4: Instalar as Dependências do Backend

Com o ambiente ativo (você deve ver `(.venv_backend)`), instale as bibliotecas:

```bash
pip install fastapi uvicorn scikit-learn pandas numpy pydantic
```

Aguarde a instalação terminar (pode demorar alguns minutos).

## * Passo 5: Gerar o Modelo de IA

Antes de iniciar o servidor, precisamos criar o arquivo de inteligência artificial.

**IMPORTANTE:** Certifique-se de estar na pasta raiz do projeto (onde está o arquivo `README.md`).

### | Windows:
```powershell
python backend/gerar_modelo.py
```

### | Linux:
```bash
python3 backend/gerar_modelo.py
```

✅ Se aparecer a mensagem **"Sucesso!"**, o modelo foi criado corretamente!



## 3️⃣ Preparar o Frontend (Site)

Agora vamos configurar a parte visual do site.

## * Passo 1: Abrir um NOVO Terminal

**⚠️ IMPORTANTE:** NÃO FECHE o terminal do Backend! Abra um novo terminal separado.

### | Windows:
1. Aperte `Windows + R`
2. Digite `cmd` e aperte Enter
3. Navegue até a pasta do projeto:
```powershell
cd C:\Users\SeuNome\Downloads\Cancer_de_mama
```

### | Linux:
1. Aperte `Ctrl + Alt + T` para abrir um novo terminal
2. Navegue até a pasta do projeto:
```bash
cd ~/Downloads/Cancer_de_mama
```

## * Passo 2: Entrar na Pasta do Frontend

Agora vamos entrar especificamente na pasta do frontend:

### | Windows:
```powershell
cd frontend
```

### | Linux:
```bash
cd frontend
```

## * Passo 3: Criar o Ambiente Virtual do Frontend

### | Windows:
```powershell
python -m venv .venv_frontend
```

### | Linux:
```bash
python3 -m venv .venv_frontend
```

## * Passo 4: Ativar o Ambiente Virtual

### | Windows:
```powershell
.\.venv_frontend\Scripts\activate
```

### | Linux:
```bash
source .venv_frontend/bin/activate
```

✅ **Como saber se funcionou?**  
O terminal deve mostrar `(.venv_frontend)` no começo da linha.

## * Passo 5: Instalar as Dependências do Frontend

Com o ambiente ativo, instale o Django e outras bibliotecas:

```bash
pip install django pillow requests
```

* `django`: Framework principal do site
* `pillow`: Para trabalhar com imagens (mamografias)
* `requests`: Para comunicação com o backend

## 🛠️ Passo 6: Configurar o Banco de Dados

O Django precisa criar um pequeno banco de dados local.

### | Windows:
```powershell
python manage.py migrate
```

### | Linux:
```bash
python3 manage.py migrate
```

✅ Se aparecerem várias linhas com **OK** verde, deu certo!

## 4️⃣ Rodar o Projeto

Agora vamos colocar tudo no ar! Você precisará de **2 terminais abertos**.

## 🖥️ Terminal 1: Backend (API)

1. Abra o primeiro terminal
2. Navegue até a pasta raiz do projeto
3. Ative o ambiente virtual do backend:

### | Windows:
```powershell
cd C:\Users\SeuNome\Downloads\Cancer_de_mama
.\.venv_backend\Scripts\activate
```

### | Linux:
```bash
cd ~/Downloads/Cancer_de_mama
source .venv_backend/bin/activate
```

4. Inicie o servidor backend:
```bash
uvicorn backend.api:app --reload
```

✅ Você deve ver uma mensagem verde:
```
INFO: Uvicorn running on http://127.0.0.1:8000
```

**⚠️ MANTENHA ESTE TERMINAL ABERTO!** Se fechar, a API para de funcionar.

## 🌐 Terminal 2: Frontend (Site)

1. Abra um segundo terminal
2. Navegue até a pasta do frontend
3. Ative o ambiente virtual do frontend:

### | Windows:
```powershell
cd C:\Users\SeuNome\Downloads\Cancer_de_mama\frontend
.\.venv_frontend\Scripts\activate
```

### | Linux:
```bash
cd ~/Downloads/Cancer_de_mama/frontend
source .venv_frontend/bin/activate
```

4. Inicie o servidor Django (na porta 8001 para não conflitar com o backend):

### | Windows:
```powershell
python manage.py runserver 8001
```

### | Linux:
```bash
python3 manage.py runserver 8001
```

✅ Você deve ver:
```
Starting development server at http://127.0.0.1:8001/
```

**⚠️ MANTENHA ESTE TERMINAL ABERTO TAMBÉM!**

## 🧪 Acessar a Aplicação

Agora você tem os dois servidores rodando:

### Backend (API):
Abra seu navegador e acesse: **http://127.0.0.1:8000/docs**

Você verá a documentação interativa da API (Swagger UI - tela azul).

### Frontend (Site):
Abra outra aba do navegador e acesse: **http://127.0.0.1:8001**

Você verá a interface de upload de imagens! 🎉


## 5️⃣ Solução de Problemas

## ❌ Erro: "python não é reconhecido como comando"

### | Windows:
Você esqueceu de marcar "Add Python to PATH" na instalação. Soluções:

1. **Opção 1:** Reinstale o Python marcando a opção
2. **Opção 2:** Use `py` no lugar de `python`:
```powershell
py -m venv .venv_backend
```

### | Linux:
Use `python3` em vez de `python`:
```bash
python3 -m venv .venv_backend
```

## ❌ Erro: "Porta 8000 já está em uso"

Outro programa está usando a porta 8000. Soluções:

### Opção 1: Usar outra porta
```bash
uvicorn backend.api:app --reload --port 8002
```

### Opção 2: Encontrar e fechar o programa que usa a porta

**Windows:**
```powershell
netstat -ano | findstr :8000
```
Anote o número PID e mate o processo:
```powershell
taskkill /PID numero_do_pid /F
```

**Linux:**
```bash
lsof -i :8000
```
Mate o processo:
```bash
kill -9 PID_numero
```

## ❌ Erro: "Modelo não encontrado"

Você esqueceu de gerar o modelo. Volte ao [Passo 5 do Backend](#🧠-passo-5-gerar-o-modelo-de-ia).

## ❌ Erro: "Module not found" ou "No module named..."

Você não instalou as dependências corretamente. Certifique-se de:

1. O ambiente virtual está ativo (você vê `(.venv_backend)` ou `(.venv_frontend)`)
2. Rode os comandos `pip install` novamente

## ❌ Erro de CSRF Token no Upload

Se ao enviar imagens aparecer erro de CSRF:

1. Limpe o cache do navegador
2. Feche e abra o navegador novamente
3. Acesse o site novamente

## 🆘 Precisa de Ajuda?

Se encontrou algum problema não listado aqui:

1. Leia a mensagem de erro com atenção
2. Copie a mensagem completa
3. Procure no Google: "nome do erro + python django" ou "nome do erro + fastapi"
4. Entre em contato com a equipe do projeto

## 👥 Equipe

- Marcos Paulo
- Nicolas do Vale
- Pedro Priori
- Raica Lyra
- Renato Nascimento
- Victor Gabriel

## 📝 Resumo Rápido dos Comandos

## Iniciar o Backend:
```bash
# 1. Navegar até a pasta raiz
cd caminho/para/Cancer_de_mama

# 2. Ativar ambiente (Windows)
.\.venv_backend\Scripts\activate

# 2. Ativar ambiente (Linux)
source .venv_backend/bin/activate

# 3. Rodar servidor
uvicorn backend.api:app --reload
```

## Iniciar o Frontend:
```bash
# 1. Navegar até a pasta frontend
cd caminho/para/Cancer_de_mama/frontend

# 2. Ativar ambiente (Windows)
.\.venv_frontend\Scripts\activate

# 2. Ativar ambiente (Linux)
source .venv_frontend/bin/activate

# 3. Rodar servidor (Windows)
python manage.py runserver 8001

# 3. Rodar servidor (Linux)
python3 manage.py runserver 8001
```
