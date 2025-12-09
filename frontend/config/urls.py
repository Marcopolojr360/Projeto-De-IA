from django.contrib import admin # Importa a view do painel administrativo
from django.urls import path, include # 'path' para definir URLs, 'include' para incluir URLs de outros apps
from django.conf import settings # Acesso às configurações (como DEBUG, MEDIA_URL)
from django.conf.urls.static import static # Função para servir arquivos estáticos/media

# Lista principal de mapeamento de URLs
urlpatterns = [
    # 1. Rota do Administrador
    # Mapeia a URL /admin/ para o painel de administração do Django
    path('admin/', admin.site.urls),
    
    # 2. Rota do Aplicativo 'upload_imagens'
    # Mapeia a URL base (vazio, '') para as URLs definidas no aplicativo 'upload_imagens'
    # Todo o tráfego que não for '/admin' será enviado para 'upload_imagens/urls.py'
    path('', include('upload_imagens.urls')), 
]

# 3. Configuração de Arquivos de Mídia (Apenas em Desenvolvimento)
# Este bloco é essencial para permitir que o Django sirva os arquivos de upload
# (imagens) quando o DEBUG está ativado (ou seja, em ambiente de desenvolvimento).
if settings.DEBUG:
    # Adiciona uma nova entrada de URL à lista urlpatterns
    urlpatterns += static(
        settings.MEDIA_URL,          # Define a URL base para arquivos de mídia (ex: /media/)
        document_root=settings.MEDIA_ROOT # Define o diretório onde os arquivos de mídia estão salvos
    )
    # Importante: Em produção, o servidor web (Nginx/Apache) deve ser configurado
    # para servir os arquivos de mídia diretamente, e este bloco deve ser ignorado.