from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os
from datetime import datetime
from .services import obter_predicao_api

def upload_page(request):
    return render(request, 'upload.html')

def format_filesize(size_bytes):
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
            # 1. Salvar imagens fisicamente
            path1 = default_storage.save(f'uploads/{image1.name}', ContentFile(image1.read()))
            path2 = default_storage.save(f'uploads/{image2.name}', ContentFile(image2.read()))
            
            full_path1 = os.path.join(settings.MEDIA_ROOT, path1)
            full_path2 = os.path.join(settings.MEDIA_ROOT, path2)

            # 2. Executar IA (Localmente via services.py)
            pred1 = obter_predicao_api(full_path1)
            pred2 = obter_predicao_api(full_path2)

            # 3. Preparar URLs para exibição
            url1 = os.path.join(settings.MEDIA_URL, path1).replace('\\', '/')
            url2 = os.path.join(settings.MEDIA_URL, path2).replace('\\', '/')

            # 4. Salvar na sessão
            request.session['analise'] = {
                'imagem1': {
                    'url': url1,
                    'nome': image1.name,
                    'tamanho': format_filesize(image1.size),
                    'prediction': pred1.get('predicted_class', 'Erro'),
                    'confidence': round(float(pred1.get('confidence', 0)) * 100, 2)
                },
                'imagem2': {
                    'url': url2,
                    'nome': image2.name,
                    'tamanho': format_filesize(image2.size),
                    'prediction': pred2.get('predicted_class', 'Erro'),
                    'confidence': round(float(pred2.get('confidence', 0)) * 100, 2)
                },
                'timestamp': datetime.now().strftime('%d/%m/%Y às %H:%M'),
                'model_name': 'Random Forest (Processamento Local)',
            }
            
            return JsonResponse({
                'success': True,
                'message': 'Análise realizada com sucesso!',
                'redirect_url': '/resultado/'
            })
            
        except Exception as e:
            print(f"Erro no processamento: {e}")
            return JsonResponse({'success': False, 'message': f'Erro interno: {str(e)}'}, status=500)
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'}, status=405)

def resultado_view(request):
    analise = request.session.get('analise')
    if not analise:
        return redirect('upload_page')
    return render(request, 'resultado.html', analise)