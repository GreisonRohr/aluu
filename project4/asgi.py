
# Importa o módulo `dotenv` para carregar as variáveis de ambiente a partir de um arquivo `.env`
import dotenv
import os

# Carrega as variáveis de ambiente do arquivo `.env`
dotenv.load_dotenv()

# Importa a função `get_asgi_application` do módulo `django.core.asgi` para obter a aplicação ASGI do Django
from django.core.asgi import get_asgi_application

# Define o valor padrão para a variável de ambiente `DJANGO_SETTINGS_MODULE`
# como `project4.settings`, indicando o módulo de configurações do Django a ser usado
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project4.settings')

# Obtém a aplicação ASGI do Django
application = get_asgi_application()
