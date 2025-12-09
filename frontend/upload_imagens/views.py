from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import requests
from datetime import datetime

# URL da sua API FastAPI (conforme api.py)
API_URL = "http://127.0.0.1:8000/predict"

def upload_page(request):
    return render(request, 'upload.html')

def upload_images(request):
    if request.method == 'POST':
        try:
            # 1. Obter dados do formulário (JSON)
            data = json.loads(request.body)
            
            # CORREÇÃO: Remover o token CSRF antes de converter
            if 'csrfmiddlewaretoken' in data:
                del data['csrfmiddlewaretoken']
            
            # Agora sim, converte apenas as medidas numéricas
            payload = {k: float(v) for k, v in data.items()}

            # 2. Enviar para a API FastAPI
            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 200:
                api_result = response.json()
                
                # Traduzir classes
                classe_predita = api_result.get('predicted_class', '')
                if classe_predita == 'B':
                    classe_display = 'Benigno'
                    cor = 'green'
                elif classe_predita == 'M':
                    classe_display = 'Maligno'
                    cor = 'red'
                else:
                    classe_display = 'Desconhecido'
                    cor = 'gray'

                # Formatar confiança
                confidence = api_result.get('confidence', 0) * 100

                # 3. Salvar na sessão para exibir no resultado.html
                request.session['analise'] = {
                    'tipo': 'numerica', # Flag para o template saber que não tem imagem
                    'resultado': classe_display,
                    'probabilidade': round(confidence, 2),
                    'cor': cor,
                    'dados_input': payload, # Opcional: mostrar os dados inseridos
                    'timestamp': datetime.now().strftime('%d/%m/%Y às %H:%M'),
                    'model_name': 'Random Forest (Via FastAPI)',
                }

                return JsonResponse({
                    'success': True,
                    'message': 'Análise realizada com sucesso!',
                    'redirect_url': '/resultado/'
                })
            else:
                return JsonResponse({'success': False, 'message': f'Erro na API: {response.text}'}, status=500)

        except Exception as e:
            print(f"Erro no processamento: {e}")
            return JsonResponse({'success': False, 'message': f'Erro interno: {str(e)}'}, status=500)
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'}, status=405)

def resultado_view(request):
    analise = request.session.get('analise')
    if not analise:
        return redirect('upload_page')
    return render(request, 'resultado.html', analise)