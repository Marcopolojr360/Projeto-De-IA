from django.urls import path
from . import views

urlpatterns = [
    # Rota 1: Página Inicial
    # Quando a URL for vazia (''), chama a função upload_page na views.py
    path('', views.upload_page, name='upload_page'),
    
    # Rota 2: API Interna de Análise
    # URL '/analyze/' recebe os dados do formulário via POST e chama analyze_data
    path('analyze/', views.analyze_data, name='analyze'),
    
    # Rota 3: Página de Resultados
    # URL '/resultado/' exibe o relatório final chamando resultado_view
    path('resultado/', views.resultado_view, name='resultado'),
]