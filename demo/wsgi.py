import os
import time
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

# Указываем настройки твоего проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo.settings')

# Инициализируем приложение Django
application = get_wsgi_application()

# Код ниже запускает миграции (создает таблицы в базе Neon)
try:
    print("Vercel startup: Running migrations...")
    call_command('migrate', interactive=False)
    print("Vercel startup: Migrations finished!")
except Exception as e:
    print(f"Vercel startup: Migration failed: {e}")

# Это нужно для Vercel (он ищет переменную app)
app = application