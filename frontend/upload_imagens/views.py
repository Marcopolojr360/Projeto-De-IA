# views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os
from datetime import datetime

# ... (funções format_filesize e predict_cancer omitidas por brevidade, mas devem estar no arquivo)

def upload_page(request):
    """Renderiza a página de upload"""
    return render(request, 'upload.html')

def upload_images(request):
    """Processa o upload das duas imagens"""
    if request.method == 'POST':
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        
        if not image1 or not image2:
            return JsonResponse({
                'success': False,
                'message': 'Por favor, envie ambas as imagens'
            }, status=400)
        
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        
        for img, name in [(image1, 'Imagem 1'), (image2, 'Imagem 2')]:
            ext = os.path.splitext(img.name)[1].lower()
            if ext not in allowed_extensions:
                return JsonResponse({
                    'success': False,
                    'message': f'{name} deve ser uma imagem válida (JPG, PNG, GIF ou WEBP)'
                }, status=400)
        
        try:
            # Salva as imagens
            path1 = default_storage.save(f'uploads/{image1.name}', ContentFile(image1.read()))
            path2 = default_storage.save(f'uploads/{image2.name}', ContentFile(image2.read()))
            
            # Obtém URLs completas
            # A url real dependeria da sua configuração de MEDIA_URL/MEDIA_ROOT.
            # Vou manter a simulação:
            url1 = os.path.join(settings.MEDIA_URL, path1).replace('\\', '/')
            url2 = os.path.join(settings.MEDIA_URL, path2).replace('\\', '/')

            # Dados simulados para demonstração
            resultado1 = {
                'prediction': 'Benigno',
                'confidence': 87.5
            }
            resultado2 = {
                'prediction': 'Maligno',
                'confidence': 92.3
            }

            # INCLUI model_name e processing_time na sessão
            request.session['analise'] = {
                'imagem1': {
                    'url': url1,
                    'nome': image1.name,
                    'tamanho': format_filesize(image1.size),
                    'prediction': resultado1['prediction'],
                    'confidence': resultado1['confidence']
                },
                'imagem2': {
                    'url': url2,
                    'nome': image2.name,
                    'tamanho': format_filesize(image2.size),
                    'prediction': resultado2['prediction'],
                    'confidence': resultado2['confidence']
                },
                'timestamp': datetime.now().strftime('%d/%m/%Y às %H:%M'),
                'model_name': 'CNN-V1',
                'processing_time': '2.3s'
            }
            
            return JsonResponse({
                'success': True,
                'message': 'Imagens enviadas com sucesso!',
                'redirect_url': '/resultado/'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro ao processar imagens: {str(e)}'
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'message': 'Método não permitido'
    }, status=405)


def resultado_view(request):
    """View para exibir os resultados da análise"""
    # Recupera os dados da sessão
    analise = request.session.get('analise')
    
    if not analise:
        # CORRIGIDO: Redireciona para 'upload_page' (a página inicial/upload GET)
        return redirect('upload_page')
    
    context = {
        'imagem1': analise['imagem1'],
        'imagem2': analise['imagem2'],
        'timestamp': analise['timestamp'],
        # Variáveis agora recuperadas da sessão
        'model_name': analise['model_name'],
        'processing_time': analise['processing_time']
    }
    
    return render(request, 'resultado.html', context)


# Funções de utilidade que faltavam no arquivo original, mas são necessárias
def format_filesize(size_bytes):
    """Formata o tamanho do arquivo para exibição"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def predict_cancer(image_path):
    """
    Função de exemplo para integração com modelo de ML
    Substitua com sua implementação real
    """
    
    import random
    pred = random.choice(['Benigno', 'Maligno'])
    conf = round(random.uniform(75, 98), 1)
    return {'prediction': pred, 'confidence': conf}