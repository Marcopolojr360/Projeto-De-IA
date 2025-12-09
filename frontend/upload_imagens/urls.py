from django.urls import path
from . import views

urlpatterns = [
    # Rota 1: Página Inicial / Formulário de entrada de dados
    path('', views.upload_page, name='upload_page'),
    
    # Rota 2: Processamento da Análise (recebe JSON via POST)
    path('analyze/', views.analyze_data, name='analyze'),
    
    # Rota 3: Página de Resultados
    path('resultado/', views.resultado_view, name='resultado'),
]