
import requests # Biblioteca para fazer a conexão HTTP com o backend

# URL da API do Backend (FastAPI)
# Certifique-se de que o backend esteja rodando nesta porta
API_URL = "http://127.0.0.1:8000/predict"

def obter_predicao_api(dados_paciente):
    """
    Função responsável por enviar os dados clínicos para a IA.
    """
    try:
        # Enviamos os dados brutos recebidos do formulário diretamente para a API.
        # O timeout evita que o site trave se a IA demorar demais.
        response = requests.post(API_URL, json=dados_paciente, timeout=10)
        
      
        if response.status_code == 200:
            # Sucesso: A IA devolveu o diagnóstico
            resultado = response.json()
            
            return {
                'success': True,
                'prediction': resultado.get('predicted_class', 'Desconhecido'),
                # Convertemos a confiança (0.98) para porcentagem legível (98.0%)
                'confidence': round(resultado.get('confidence', 0) * 100, 2)
            }
        else:
            # Erro na validação ou processamento do Backend
            error_msg = f"A API retornou erro: {response.status_code}"
            print(error_msg)
            return {
                'success': False, 
                'error': error_msg
            }

    except requests.exceptions.ConnectionError:
        # Acontece se o Backend (FastAPI) estiver desligado.
        msg = "Não foi possível conectar ao servidor de Inteligência Artificial."
        print(f"Erro: {msg}")
        return {'success': False, 'error': msg}

    except Exception as e:
        msg = f"Erro interno ao processar solicitação: {str(e)}"
        print(msg)
        return {'success': False, 'error': msg}