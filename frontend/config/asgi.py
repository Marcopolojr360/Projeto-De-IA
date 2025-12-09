"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os # Módulo para interagir com o sistema operacional

from django.core.asgi import get_asgi_application # Função do Django para obter o objeto ASGI principal

# 1. Configuração do Ambiente
# Define a variável de ambiente DJANGO_SETTINGS_MODULE.
# Isso informa ao Django qual arquivo de configurações ele deve usar.
# O servidor ASGI (como Daphne ou Uvicorn) usará esta informação para inicializar o Django.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# 2. Obtenção do Aplicativo ASGI
# O objeto 'application' é o ponto de entrada (callable) que o servidor ASGI usará
# para rotear requisições para o seu projeto Django.
application = get_asgi_application()