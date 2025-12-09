from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import datetime
import json
import requests

# Endereço da IA que sabe interpretar os números (Raio, Textura, etc.)
API_URL = "http://127.0.0.1:8000/predict"

def upload_page(request):
    """
    Rota '/'
    Renderiza o formulário (upload.html) onde o médico/usuário digita
    manualmente os 30 valores numéricos dos exames.
    """
    return render(request, 'upload.html')

def analyze_data(request):
    """
    Rota '/analyze/' (POST)
    Recebe o JSON com os números digitados no formulário.
    """
    if request.method == 'POST':
        try:
            # 1. RECEBE OS DADOS MANUAIS
            # O 'request.body' contém o JSON enviado pelo JavaScript do formulário.
            data = json.loads(request.body)
                        
            # 2. CONSULTA A INTELIGÊNCIA ARTIFICIAL
            # Envia esses mesmos números para o Backend (FastAPI).
            # O Backend usa o modelo treinado (Decision Tree) para classificar.
            response = requests.post(API_URL, json=data, timeout=10)
            
            if response.status_code == 200:
                prediction_result = response.json()
                
                # 3. GUARDA O RESULTADO
                # Salva o diagnóstico (Maligno/Benigno) na sessão do navegador.
                request.session['analise'] = {
                    'resultado': {
                        'prediction': prediction_result['predicted_class'],
                        'confidence': round(prediction_result['confidence'] * 100, 2)
                    },
                    'dados_entrada': data, # Salva os números digitados para referência
                    'timestamp': datetime.now().strftime('%d/%m/%Y às %H:%M'),
                    'model_name': 'Decision Tree (Árvore de Decisão)'
                }
                
                return JsonResponse({
                    'success': True,
                    'message': 'Análise realizada com sucesso!',
                    'redirect_url': '/resultado/'
                })
            else:
                return JsonResponse({'success': False, 'message': 'Erro na API'}, status=500)
                
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
    return JsonResponse({'success': False}, status=405)

def resultado_view(request):
    """
    Rota '/resultado/'
    Exibe o diagnóstico final.
    """
    analise = request.session.get('analise')
    
    if not analise:
        return redirect('upload_page')
    
    resultado = analise.get('resultado', {})
    prediction = resultado.get('prediction', 'Erro')
    confidence = resultado.get('confidence', 0)
    
    context = {
        'imagem1': {
            'prediction': prediction, # Ex: "Maligno"
            'confidence': confidence, # Ex: 99.5%
            'nome': 'Dados de Entrada 1', # Rótulo genérico para o card da esquerda
        },
        'imagem2': {
            'prediction': prediction,
            'confidence': confidence,
            'nome': 'Dados de Entrada 2', # Rótulo genérico para o card da direita
        },
        'timestamp': analise.get('timestamp', ''),
        'model_name': analise.get('model_name', 'Decision Tree')
    }
    
    return render(request, 'resultado.html', context)