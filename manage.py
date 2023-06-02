
import os
import sys


def main():
    # Define a variável de ambiente DJANGO_SETTINGS_MODULE para especificar o arquivo de configurações do projeto Django.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto.settings')
    try:
        # Tenta importar a função execute_from_command_line do módulo django.core.management
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Não foi possível importar o Django. Tem certeza de que ele está instalado e "
            "disponível em sua variável de ambiente PYTHONPATH? Você "
            "esqueceu de ativar um ambiente virtual?"
        ) from exc
    # Chama a função execute_from_command_line com os argumentos da linha de comando (sys.argv) para iniciar o aplicativo Django.
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
