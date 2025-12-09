#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
# Linha shebang padrão que indica o interpretador a ser usado (importante em sistemas Unix-like)
import os # Módulo para interagir com o sistema operacional
import sys # Módulo para acessar variáveis e funções relacionadas ao interpretador

def main():
    """Executa tarefas administrativas do Django."""
    
    # 1. Configuração do Ambiente
    # Define a variável de ambiente DJANGO_SETTINGS_MODULE
    # Isso informa ao Django qual arquivo de configurações ele deve usar (neste caso, 'config.settings')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    # 2. Execução
    try:
        # Tenta importar a função principal de execução de comandos do Django
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # 3. Tratamento de Erro (Django não instalado/encontrado)
        # Se o Django não puder ser importado, lança um erro com instruções úteis
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
        
    # Executa o comando que o usuário digitou na linha de comando
    # sys.argv é a lista de argumentos passados para o script (ex: ['manage.py', 'runserver', '8000'])
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    # O bloco de código principal que chama a função 'main'
    main()