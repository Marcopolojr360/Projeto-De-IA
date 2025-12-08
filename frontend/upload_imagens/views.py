from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os
from datetime import datetime
# Importar o serviço que criamos
from .services import obter_predicao_api

def upload_page(request):
    return render(request, 'upload.html')

def format_filesize(size_bytes):
    """Formata o tamanho do arquivo para exibição"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

def upload_images(request):
    if request.method == 'POST':
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        
        if not image1 or not image2:
            return JsonResponse({'success': False, 'message': 'Por favor, envie ambas as imagens'}, status=400)
        
        try:
            # 1. Salvar imagens
            path1 = default_storage.save(f'uploads/{image1.name}', ContentFile(image1.read()))
            path2 = default_storage.save(f'uploads/{image2.name}', ContentFile(image2.read()))
            
            full_path1 = os.path.join(settings.MEDIA_ROOT, path1)
            full_path2 = os.path.join(settings.MEDIA_ROOT, path2)

            # 2. Chamar a API Backend (Integração Real)
            pred1 = obter_predicao_api(full_path1)
            pred2 = obter_predicao_api(full_path2)

            # Fallback caso a API esteja offline (para não quebrar a demo)
            if not pred1:
                pred1 = {'predicted_class': 'Erro API', 'confidence': 0.0}
            if not pred2:
                pred2 = {'predicted_class': 'Erro API', 'confidence': 0.0}

            # 3. Preparar URLs para exibição
            url1 = os.path.join(settings.MEDIA_URL, path1).replace('\\', '/')
            url2 = os.path.join(settings.MEDIA_URL, path2).replace('\\', '/')

            # 4. Salvar na sessão
            request.session['analise'] = {
                'imagem1': {
                    'url': url1,
                    'nome': image1.name,
                    'tamanho': format_filesize(image1.size),
                    'prediction': pred1['predicted_class'],
                    'confidence': float(pred1['confidence']) * 100 if pred1['confidence'] <= 1 else float(pred1['confidence'])
                },
                'imagem2': {
                    'url': url2,
                    'nome': image2.name,
                    'tamanho': format_filesize(image2.size),
                    'prediction': pred2['predicted_class'],
                    'confidence': float(pred2['confidence']) * 100 if pred2['confidence'] <= 1 else float(pred2['confidence'])
                },
                'timestamp': datetime.now().strftime('%d/%m/%Y às %H:%M'),
                'model_name': 'RandomForest (Via FastAPI)',
                'processing_time': 'API Request'
            }
            
            return JsonResponse({
                'success': True,
                'message': 'Análise realizada com sucesso!',
                'redirect_url': '/resultado/'
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Erro: {str(e)}'}, status=500)
    
    return JsonResponse({'success': False, 'message': 'Método inválido'}, status=405)

def resultado_view(request):
    analise = request.session.get('analise')
    if not analise:
        return redirect('upload_page')
    
    # Passa o contexto diretamente, pois já está formatado
    return render(request, 'resultado.html', analise)