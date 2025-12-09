from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import datetime
import json
import requests

# URL da API FastAPI
API_URL = "http://127.0.0.1:8000/predict"

def upload_page(request):
    """
    Renderiza o template HTML do formulário de entrada de dados.
    Mapeada para a URL: /
    """
    return render(request, 'upload.html')

def analyze_data(request):
    """
    Lida com o envio de dados via POST.
    Mapeada para a URL: /analyze/
    """
    if request.method == 'POST':
        try:
            # Pegar os dados JSON do corpo da requisição
            data = json.loads(request.body)
            
            print(f"Dados recebidos: {data}")  # Debug
            
            # Fazer requisição para a API FastAPI
            response = requests.post(API_URL, json=data, timeout=10)
            
            print(f"Status da API: {response.status_code}")  # Debug
            
            if response.status_code == 200:
                prediction_result = response.json()
                
                print(f"Resultado da predição: {prediction_result}")  # Debug
                
                # Salvar resultado na sessão
                request.session['analise'] = {
                    'resultado': {
                        'prediction': prediction_result['predicted_class'],
                        'confidence': round(prediction_result['confidence'] * 100, 2)
                    },
                    'dados_entrada': data,
                    'timestamp': datetime.now().strftime('%d/%m/%Y às %H:%M'),
                    'model_name': 'Decision Tree (Árvore de Decisão)'
                }
                
                return JsonResponse({
                    'success': True,
                    'message': 'Análise realizada com sucesso!',
                    'redirect_url': '/resultado/'
                })
            else:
                error_msg = f'Erro na API: Status {response.status_code}'
                print(error_msg)
                return JsonResponse({
                    'success': False,
                    'message': error_msg
                }, status=500)
                
        except requests.exceptions.RequestException as e:
            print(f"Erro de conexão com a API: {e}")
            return JsonResponse({
                'success': False,
                'message': f'Erro ao conectar com a API: {str(e)}'
            }, status=500)
        except Exception as e:
            print(f"Erro no processamento: {e}")
            import traceback
            traceback.print_exc()
            return JsonResponse({
                'success': False,
                'message': f'Erro interno: {str(e)}'
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'message': 'Método não permitido'
    }, status=405)

def resultado_view(request):
    """
    Renderiza o template de resultados, utilizando os dados salvos na sessão.
    Mapeada para a URL: /resultado/
    """
    analise = request.session.get('analise')
    
    if not analise:
        return redirect('upload_page')
    
    # Preparar dados para o template
    resultado = analise.get('resultado', {})
    prediction = resultado.get('prediction', 'Erro')
    confidence = resultado.get('confidence', 0)
    
    context = {
        'imagem1': {
            'prediction': prediction,
            'confidence': confidence,
            'nome': 'Dados de Entrada 1',
        },
        'imagem2': {
            'prediction': prediction,
            'confidence': confidence,
            'nome': 'Dados de Entrada 2',
        },
        'timestamp': analise.get('timestamp', ''),
        'model_name': analise.get('model_name', 'Decision Tree')
    }
    
    return render(request, 'resultado.html', context)