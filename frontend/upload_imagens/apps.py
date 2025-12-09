from django.apps import AppConfig # Importa a classe base para a configuração de aplicativos

# Define a classe de configuração específica para este aplicativo
class UploadImagensConfig(AppConfig):
    """
    Configuração do aplicativo 'upload_imagens'.
    """
    
    # Define o tipo de campo de chave primária padrão para os modelos
    # 'django.db.models.BigAutoField' é o tipo recomendado para novas aplicações no Django 3.2+
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Define o nome do aplicativo. 
    # Este é o nome que deve ser listado em INSTALLED_APPS no settings.py do projeto principal.
    name = 'upload_imagens'