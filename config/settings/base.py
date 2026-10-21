from pathlib import Path
from environ import Env

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = Env(
    PYTHON_ENV = (str, ''),

    SECRET_KEY = (str, ''),
    ALLOWED_HOSTS = (list, []),

    DB_USER = (str, ''),
    DB_PASSWORD = (str, ''),
    DB_HOST = (str, ''),
    DB_PORT = (int, 0),
    DB_NAME = (str, ''),

    S3_ENDPOINT = (str, ''),
    S3_ACCESS_KEY = (str, ''),
    S3_SECRET_KEY = (str, ''),
    S3_BUCKET = (str, ''),

    SMTP_USER = (str, ''),
    SMTP_PASSWORD = (str, ''),
    SMTP_HOST = (str, ''),
    SMTP_PORT = (int, 0),
    SMTP_STARTTLS = (bool, False)
)

PYTHON_ENV = env.str('PYTHON_ENV')

SECRET_KEY = env.str('SECRET_KEY')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

DB_USER = env.str('DB_USER')

DB_PASSWORD = env.str('DB_PASSWORD')

DB_HOST = env.str('DB_HOST')

DB_PORT = env.int('DB_PORT')

DB_NAME = env.str('DB_NAME')

S3_ENDPOINT = env.str('S3_ENDPOINT')

S3_ACCESS_KEY = env.str('S3_ACCESS_KEY')

S3_SECRET_KEY = env.str('S3_SECRET_KEY')

S3_BUCKET = env.str('S3_BUCKET')

SMTP_USER = env.str('SMTP_USER')

SMTP_PASSWORD = env.str('SMTP_PASSWORD')

SMTP_HOST = env.str('SMTP_HOST')

SMTP_PORT = env.int('SMTP_PORT')

SMTP_STARTTLS = env.bool('SMTP_STARTTLS')

DEBUG = PYTHON_ENV == 'development'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tailwind',
    'apps.accounts',
    'apps.core',
    'apps.fields',
    'apps.schemas',
    'apps.theme'
]

TAILWIND_APP_NAME = 'apps.theme'

TAILWIND_USE_STANDALONE_BINARY = True

SERIALIZATION_MODULES = {
    'yml': 'django.core.serializers.pyyaml',
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

CONTEXT_PROCESSORS = [
    'django.template.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [BASE_DIR / 'templates', *sorted(BASE_DIR.glob('apps/*/templates'))],
        'OPTIONS': {
            'environment': 'config.jinja2.environment',
            'context_processors': CONTEXT_PROCESSORS,
        },
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {'context_processors': CONTEXT_PROCESSORS},
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {}
}

AUTH_USER_MODEL = 'accounts.User'

AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator' }
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'public'

STATICFILES_DIRS = [BASE_DIR / 'static']

MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend'
    }
}