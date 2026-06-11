import os
from pathlib import Path
import dj_database_url  # Нужно добавить в requirements.txt

# Базовая директория проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# БЕЗОПАСНОСТЬ: В идеале вынести в переменные окружения Vercel
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-me-please')

# На Vercel DEBUG лучше держать True только при разработке
DEBUG = True

# Добавляем домены Vercel, чтобы авторизация не выдавала ошибку 403
ALLOWED_HOSTS = ['*', '.vercel.app']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cafe', 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Четко после SecurityMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'demo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'demo.wsgi.application'

# БАЗА ДАННЫХ
# На Vercel файловая система только для чтения. SQLite будет сбрасываться.
# Этот код автоматически использует Postgres, если он подключен в Vercel, 
# или SQLite, если ты запускаешь проект локально.
DATABASE_URL = os.environ.get('POSTGRES_URL')

DATABASES = {
    'default': dj_database_url.config(
        default=DATABASE_URL if DATABASE_URL else f"sqlite:///{os.path.join(BASE_DIR, 'db.sqlite3')}",
        conn_max_age=600
    )
}

# Валидация паролей
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
]

# Язык и время
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# --- СТАТИКА (ГЛАВНОЕ ДЛЯ UNITY) ---
STATIC_URL = '/static/'

# Путь к папке со статикой внутри твоего приложения cafe
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'cafe', 'static'),
]

# Папка, куда соберется вся статика при деплое (создастся сама)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Настройка WhiteNoise для работы на Vercel (обработка кэша и сжатия)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Медиа файлы
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- АВТОРИЗАЦИЯ ---
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/login/'

# Настройки безопасности для Vercel (чтобы работал логин)
CSRF_TRUSTED_ORIGINS = ['https://*.vercel.app']
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Настройки для Unity (разрешаем запуск в iframe, если нужно)
X_FRAME_OPTIONS = 'SAMEORIGIN'