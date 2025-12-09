"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os # Módulo para interagir com o sistema operacional

from django.core.wsgi import get_wsgi_application # Função do Django para obter o objeto WSGI principal

# 1. Configuração do Ambiente
# Define a variável de ambiente DJANGO_SETTINGS_MODULE.
# Isso informa ao Django qual arquivo de configurações ele deve usar.
# O servidor WSGI usará esta informação para inicializar o ambiente Django.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# 2. Obtenção do Aplicativo WSGI
# O objeto 'application' é o ponto de entrada (callable) que o servidor WSGI usará
# para rotear requisições para o seu projeto Django.
application = get_wsgi_application()