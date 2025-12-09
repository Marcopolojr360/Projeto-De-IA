from django.shortcuts import render, redirect # Funções para renderizar templates e redirecionar
from django.http import JsonResponse # Usado para retornar respostas JSON (especialmente para AJAX)
from django.core.files.storage import default_storage # Gerenciador de armazenamento de arquivos (ex: disco local)
from django.core.files.base import ContentFile # Usado para envolver o conteúdo do arquivo
from django.conf import settings # Acesso às configurações do Django (MEDIA_ROOT, MEDIA_URL)
import os # Manipulação de caminhos do sistema operacional
from datetime import datetime # Para registrar o timestamp da análise
from .services import obter_predicao_api # Função para chamar o modelo de ML (local ou API)

# 1. View para a Página Inicial/Upload
def upload_page(request):
    """
    Renderiza o template HTML do formulário de upload.
    Mapeada para a URL: /
    """
    return render(request, 'upload.html')

# 2. Função Auxiliar para Formatar Tamanho do Arquivo
def format_filesize(size_bytes):
    """Converte o tamanho do arquivo de bytes para KB, MB ou GB."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

# 3. View Principal para Processamento do Upload
def upload_images(request):
    """
    Lida com o envio de imagens via POST (usado pela requisição AJAX do frontend).
    Mapeada para a URL: /upload/
    """
    if request.method == 'POST':
        # Tenta obter os arquivos do corpo da requisição
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        
        # Validação básica
        if not image1 or not image2:
            return JsonResponse({'success': False, 'message': 'Por favor, envie ambas as imagens'}, status=400)
        
        try:
            # 1. Salvar imagens fisicamente (no diretório definido por MEDIA_ROOT)
            # Lê o conteúdo do arquivo e salva na pasta 'uploads'
            path1 = default_storage.save(f'uploads/{image1.name}', ContentFile(image1.read()))
            path2 = default_storage.save(f'uploads/{image2.name}', ContentFile(image2.read()))
            
            # Constrói o caminho completo do sistema de arquivos (necessário para o processamento local)
            full_path1 = os.path.join(settings.MEDIA_ROOT, path1)
            full_path2 = os.path.join(settings.MEDIA_ROOT, path2)

            # 2. Executar IA/ML
            # Chama a função de serviço que se comunica com o modelo de predição
            pred1 = obter_predicao_api(full_path1) # Assume-se que esta função processa o caminho do arquivo
            pred2 = obter_predicao_api(full_path2)

            # 3. Preparar URLs para exibição (para o frontend)
            # Combina MEDIA_URL com o caminho salvo, ajustando barras para URLs
            url1 = os.path.join(settings.MEDIA_URL, path1).replace('\\', '/')
            url2 = os.path.join(settings.MEDIA_URL, path2).replace('\\', '/')

            # 4. Salvar Dados de Análise na Sessão do Usuário
            # A sessão permite que os dados sejam mantidos e acessados na próxima view (resultado_view)
            request.session['analise'] = {
                'imagem1': {
                    'url': url1,
                    'nome': image1.name,
                    'tamanho': format_filesize(image1.size),
                    # Obtém a classe prevista e a confiança, tratando erros
                    'prediction': pred1.get('predicted_class', 'Erro'),
                    'confidence': round(float(pred1.get('confidence', 0)) * 100, 2) # Converte para percentual
                },
                'imagem2': {
                    'url': url2,
                    'nome': image2.name,
                    'tamanho': format_filesize(image2.size),
                    'prediction': pred2.get('predicted_class', 'Erro'),
                    'confidence': round(float(pred2.get('confidence', 0)) * 100, 2)
                },
                'timestamp': datetime.now().strftime('%d/%m/%Y às %H:%M'),
                'model_name': 'Random Forest (Processamento Local)', # Exemplo de metadado
            }
            
            # Retorna uma resposta JSON de sucesso para o AJAX do frontend
            return JsonResponse({
                'success': True,
                'message': 'Análise realizada com sucesso!',
                'redirect_url': '/resultado/' # URL para onde o frontend deve navegar em seguida
            })
            
        except Exception as e:
            # Captura e loga quaisquer erros durante o processamento
            print(f"Erro no processamento: {e}")
            return JsonResponse({'success': False, 'message': f'Erro interno: {str(e)}'}, status=500)
    
    # Responde se o método HTTP não for POST
    return JsonResponse({'success': False, 'message': 'Método não permitido'}, status=405)

# 4. View para a Página de Resultados
def resultado_view(request):
    """
    Renderiza o template de resultados, utilizando os dados salvos na sessão.
    Mapeada para a URL: /resultado/
    """
    # Tenta recuperar os dados da sessão
    analise = request.session.get('analise')
    
    # Se não houver dados de análise na sessão, redireciona para a página de upload
    if not analise:
        return redirect('upload_page')
        
    # Renderiza o template 'resultado.html', passando o dicionário de análise como contexto
    return render(request, 'resultado.html', analise)