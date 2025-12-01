from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

def upload_page(request):
    """Renderiza a página de upload"""
    return render(request, 'upload.html')

@csrf_exempt
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
        
        # Validar tipo de arquivo
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        
        for img, name in [(image1, 'Imagem 1'), (image2, 'Imagem 2')]:
            ext = os.path.splitext(img.name)[1].lower()
            if ext not in allowed_extensions:
                return JsonResponse({
                    'success': False,
                    'message': f'{name} deve ser uma imagem válida (JPG, PNG, GIF ou WEBP)'
                }, status=400)
        
        try:
            # Salvar as imagens
            path1 = default_storage.save(f'uploads/{image1.name}', ContentFile(image1.read()))
            path2 = default_storage.save(f'uploads/{image2.name}', ContentFile(image2.read()))
            
            return JsonResponse({
                'success': True,
                'message': 'Imagens enviadas com sucesso!',
                'paths': {
                    'image1': path1,
                    'image2': path2
                }
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro ao salvar imagens: {str(e)}'
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'message': 'Método não permitido'
    }, status=405)