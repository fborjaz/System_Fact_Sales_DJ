import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-_fyjq%+2u$$(rf3y5vl-6ktqwsj&bc^phj4pw=ty7*!lta+a$='

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django_extensions',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'livereload',
    'django.contrib.staticfiles',
    'app.core.apps.CoreConfig',
    'app.sales.apps.SalesConfig',
    'app.purcharse.apps.PurcharseConfig',
    'app.security.apps.SecurityConfig',
    'widget_tweaks',
    'tailwind',
    'theme',
]

GRAPH_MODELS = {
    'all_applications': True,
    'group_models': True,
}

TAILWIND_APP_NAME = 'theme'

INTERNAL_IPS = ["127.0.0.1",]

NPM_BIN_PATH = r'C:\Program Files\nodejs\npm.cmd'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'app.core.middleware.AdminOnlyMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'app.core.middleware.LoginRequiredMiddleware',
    'crum.CurrentRequestUserMiddleware',
    #'livereload.middleware.LiveReloadScript',
]

SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Usar base de datos para sesiones
SESSION_COOKIE_NAME = 'sessionid'
SESSION_COOKIE_SECURE = False  # Cambia a True en producción
SESSION_COOKIE_HTTPONLY = True
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False



BROWSER_REFRESH_SECONDS = 1 

ROOT_URLCONF = 'proy_sales.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'proy_sales.wsgi.application'


DATABASES = {
    "default": {
        'ENGINE': os.environ.get("DB_ENGINE", "django.db.backends.postgresql"),
        'NAME': os.environ.get("DB_DATABASE", ""),
        'USER': os.environ.get("DB_USERNAME", ""),
        'PASSWORD': os.environ.get("DB_PASSWORD", ""),
        'HOST': os.environ.get("DB_SOCKET", ""),
        'PORT': os.environ.get("DB_PORT", "5432"),
        'ATOMIC_REQUESTS': True
    }
}
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

LANGUAGE_CODE = 'es-ec'

TIME_ZONE = 'America/Guayaquil'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/' # url de archivos estaticos
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)#carpeta fisica de archivos estaticos
MEDIA_ROOT = os.path.join(BASE_DIR,'media') # carpeta fisica de archivos de Imagenes
MEDIA_URL = '/media/' # url de imagenes

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'security.User'
LOGIN_URL = '/security/auth/login'
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'




