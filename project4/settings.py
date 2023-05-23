
import os

# Define o diretório base do projeto usando o caminho absoluto do arquivo atual
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define a chave secreta usada para criptografia e segurança do projeto Django
SECRET_KEY = '13kl@xtukpwe&xj2xoysxe9_6=tf@f8ewxer5n&ifnd46+6$%8'

DEBUG = True
# Define se o modo de depuração está ativado ou desativado
# No modo de depuração (DEBUG = True), o Django exibirá informações detalhadas sobre erros

ALLOWED_HOSTS = ['aluu.azurewebsites.net']

# Define uma lista de nomes de host válidos para este projeto Django
# A configuração atual permite apenas o host 'aluu.azurewebsites.net'


INSTALLED_APPS = [  # Definição das aplicações instaladas
    'network',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]


MIDDLEWARE = [  # Configuração dos middlewares
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'project4.urls'

# Define o módulo de configuração de URL raiz do projeto como 'project4.urls'.
# Esse módulo contém as definições de URLs principais do projeto.

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Configuração dos templates do Django

# Define as configurações de template do Django
# 'DIRS' contém diretórios adicionais de templates (vazio no exemplo)
# 'APP_DIRS' define se os diretórios de templates dos aplicativos devem ser incluídos
# 'OPTIONS' contém opções adicionais, como context_processors

WSGI_APPLICATION = 'project4.wsgi.application'

# Define o módulo de aplicação WSGI do projeto como 'project4.wsgi.application'.
# Esse módulo contém a aplicação WSGI do Django que será usada pelo servidor web.


# Configuração do banco de dados

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.getenv('DATABASE_URL'),
    }
}

# Define as configurações do banco de dados.
# No exemplo fornecido, é utilizado o banco de dados SQLite3.

AUTH_USER_MODEL = "network.User"

# Define o modelo de usuário personalizado usado pelo aplicativo "network" como modelo de usuário padrão.

# Validação de senha

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Define as validações de senha que serão aplicadas aos usuários.
# No exemplo fornecido, são utilizadas várias validações, como similaridade de atributos do usuário,
# comprimento mínimo, senha comum e senha numérica.


# Internacionalização

LANGUAGE_CODE = 'pt-br'
# Define o código do idioma usado no projeto.
# No exemplo fornecido, é usado o código 'pt-br' para portugues Brasil.

TIME_ZONE = 'America/Sao_Paulo'

# Define a zona de tempo usada no projeto.
# No exemplo fornecido, é usada a zona de tempo 'America/Sao_Paulo' para o Brasil.

USE_I18N = True

# Define se a internacionalização está ativada ou desativada.
# No exemplo fornecido, a internacionalização está ativada.

USE_L10N = True

# Define se a localização está ativada ou desativada.
# No exemplo fornecido, a localização está ativada.

USE_TZ = True

# Define se o suporte a fusos horários está ativado ou desativado.
# No exemplo fornecido, o suporte a fusos horários está ativado.


# Arquivos estáticos (CSS, JavaScript, Imagens)

MEDIA_URL = '/network/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Define a URL base para os arquivos de mídia (upload de arquivos) e o diretório raiz onde os arquivos de mídia são armazenados.

STATIC_URL = '/network/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Define a URL base para os arquivos estáticos (CSS, JavaScript, imagens) e o diretório raiz onde os arquivos estáticos são armazenados.
