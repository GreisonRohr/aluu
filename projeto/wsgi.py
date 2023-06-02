
import dotenv
import os

from django.core.wsgi import get_wsgi_application

dotenv.load_dotenv()

# Configuração do arquivo .env
# Carrega as variáveis de ambiente definidas no arquivo .env

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project4.settings')

# Define a variável de ambiente 'DJANGO_SETTINGS_MODULE' com o valor 'project4.settings'.
# Essa variável define qual arquivo de configuração do Django será usado.

application = get_wsgi_application()

# Obtém a aplicação WSGI do Django para ser usada pelo servidor web.
# Essa aplicação é responsável por lidar com as solicitações HTTP recebidas pelo servidor.