from django.urls import path # Importa a função 'path' para definir as rotas
from . import views # Importa o módulo 'views' do diretório atual (onde as funções lógicas estão)

# Lista principal que mapeia as URLs para as funções de visualização (views)
urlpatterns = [
    # Rota 1: Página Inicial / Upload
    # URL: / (vazio) - a raiz do aplicativo
    path(
        '',
        views.upload_page, # Quando acessada, chama a função views.upload_page
        name='upload_page' # Nome da rota (usado para referência em templates ou código Python)
    ),
    
    # Rota 2: Processamento do Upload
    # URL: /upload/
    path(
        'upload/',
        views.upload_images, # Esta view recebe e processa o envio dos dados (geralmente via POST)
        name='upload'
    ),
    
    # Rota 3: Página de Resultados
    # URL: /resultado/
    path(
        'resultado/',
        views.resultado_view, # Esta view exibe o resultado da análise
        name='resultado'
    ),
]