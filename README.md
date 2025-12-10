
-----
# | Detecção de Câncer de Mama com IA

Este é um projeto completo (Fullstack) que utiliza Inteligência Artificial para analisar dados de exames e auxiliar na detecção de câncer de mama. O sistema é dividido em duas partes:
1.  **Backend (API):** Onde o "cérebro" (IA) vive e processa os dados.
2.  **Frontend (Site):** Onde o usuário envia as informações e vê o resultado.

---

## | Pré-requisitos (Obrigatório)

Antes de tudo, você precisa ter o **Python** instalado.

### | Windows
1. Baixe o Python em [python.org](https://www.python.org/downloads/).
2. **| IMPORTANTE:** Na instalação, marque a caixinha **"Add Python to PATH"** antes de clicar em instalar.
3. Abra o terminal (CMD ou PowerShell) e digite `python --version` para confirmar.

### | Linux (Ubuntu/Debian)
Abra o terminal e rode:
```bash
sudo apt update
sudo apt install -y python3-full python3-pip
````

-----

## | Instalação (Passo a Passo)

Siga estes passos na ordem para configurar o projeto pela primeira vez.

### 1\. Baixar e entrar na pasta

Baixe o projeto e extraia os arquivos. Depois, abra o terminal e entre na pasta do projeto.

**Windows e Linux:**

```bash
cd Projeto-De-IA
```

*(Certifique-se de que está na pasta que tem o arquivo `requirements.txt` e a pasta `frontend`)*

-----

### 2\. Criar e Ativar o Ambiente Virtual

Isso cria uma "caixa isolada" para instalar as bibliotecas sem bagunçar seu computador.

**| Windows:**

```powershell
python -m venv venv
.\venv\Scripts\activate
```

*(Se der erro de permissão no Windows, rode `Set-ExecutionPolicy Unrestricted -Scope Process` e tente ativar de novo)*

**| Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

 **Sinal de sucesso:** O terminal mostrará `(venv)` no começo da linha.

-----

### 3\. Instalar as Bibliotecas

Com o `(venv)` ativado, instale tudo o que o projeto precisa de uma vez:

**Windows e Linux:**

```bash
pip install -r requirements.txt
```

*(Isso pode demorar um pouco. Aguarde terminar).*

-----

### 4\. Treinar e Gerar o Modelo de IA

Precisamos "ensinar" a IA e salvar o arquivo de memória dela (`.pkl`) antes de ligar o sistema.

**Windows:**

```powershell
python scripts/train_and_save_model.py
```

**Linux:**

```bash
python3 scripts/train_and_save_model.py
```

 **Sucesso:** Deve aparecer a mensagem: `Sucesso! Modelo salvo em: .../backend/model/breast_cancer_model.pkl`

-----

### 5\. Configurar o Banco de Dados do Site

O site precisa criar um pequeno banco de dados local.

**Windows:**

```powershell
python frontend/manage.py migrate
```

**Linux:**

```bash
python3 frontend/manage.py migrate
```

-----

## | Como Rodar o Projeto

Para o sistema funcionar, você precisa de **dois terminais abertos** ao mesmo tempo: um para a API e outro para o Site.

### | Terminal 1: Rodar a API (Backend)

1.  Certifique-se de estar na pasta `Projeto-De-IA`.
2.  Ative o ambiente virtual (`venv`) se não estiver ativo.
3.  Rode o comando:

<!-- end list -->

```bash
uvicorn backend.api:app --reload
```

| Se aparecer `Application startup complete`, a API está online\!
**| NÃO FECHE ESSE TERMINAL.**

### | Terminal 2: Rodar o Site (Frontend)

1.  Abra um **novo terminal**.
2.  Entre na pasta do projeto (`cd Projeto-De-IA`).
3.  Ative o ambiente virtual novamente:
      * **Windows:** `.\venv\Scripts\activate`
      * **Linux:** `source venv/bin/activate`
4.  Inicie o site:

**Windows:**

```powershell
python frontend/manage.py runserver
```

**Linux:**

```bash
python3 frontend/manage.py runserver 8001
```

| Se aparecer `Starting development server at http://127.0.0.1:8001/`, o site está online\!

-----

## | Usando o Sistema

Abra seu navegador e acesse:
- **http://127.0.0.1:8000**

Lá você verá o formulário para preencher os dados ou usar os botões de "Preencher Exemplo" para testar a detecção.

-----
## | Solução de Problemas Comuns

**Erro: "python não encontrado"**

  * No Windows, tente usar o comando `py` em vez de `python`.
  * Verifique se marcou "Add to PATH" na instalação.

**Erro: "Module not found"**

  * Você provavelmente esqueceu de ativar o ambiente virtual (`venv`) antes de rodar os comandos. Ative-o e tente de novo.

**Erro: "Port already in use"**

  * Significa que o servidor já está rodando. Verifique se você não tem outro terminal aberto rodando o projeto.

**Erro ao enviar a imagem/dados**

  * Verifique se o **Terminal 1** (API) está rodando e não deu erro vermelho. O site precisa que a API esteja ligada para funcionar.

## | Colaboradores

Este projeto é o resultado do trabalho e da dedicação de uma equipe incrível. Conheça quem fez o **Projeto** acontecer:

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/Marcopolojr360">
        <img src="https://github.com/Marcopolojr360.png" width="100px;" alt="Foto de Marcos Paulo no GitHub"/>
        <br />
        <sub><b>Marcos Paulo</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/nicosntos">
        <img src="https://github.com/nicosntos.png" width="100px;" alt="Foto de Nicolas do Vale no GitHub"/>
        <br />
        <sub><b>Nicolas do Vale </b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/Pedro-Priori">
        <img src="https://github.com/Pedro-Priori.png" width="100px;" alt="Foto de Pedro Priori no GitHub"/>
        <br />
        <sub><b>Pedro Priori</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/Raicalira">
        <img src="https://github.com/Raicalira.png" width="100px;" alt="Foto de Raica Lira no GitHub"/>
        <br />
        <sub><b>Raica Lira</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/renatoNL">
        <img src="https://github.com/renatoNL.png" width="100px;" alt="Foto de Renato Nascimento no GitHub"/>
        <br />
        <sub><b>Renato Nascimento</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/VictorGabriel-00">
        <img src="https://github.com/VictorGabriel-00.png" width="100px;" alt="Foto de Victor Gabriel no GitHub"/>
        <br />
        <sub><b>Victor Gabriel</b></sub>
      </a>
    </td>
  </tr>
</table>


<!-- end list -->
