import os
import time
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command
from django.contrib.auth import get_user_model

# Настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo.settings')

# Инициализация приложения
application = get_wsgi_application()

def setup_app():
    try:
        # 1. Запуск миграций (создание таблиц)
        print("Running migrations...")
        call_command('migrate', interactive=False)
        
        # 2. Создание админа
        User = get_user_model()
        # Если пользователя admin нет - создаем. Если есть - ставим пароль admin12345
        user, created = User.objects.get_or_create(username='admin')
        user.set_password('admin12345')
        user.is_superuser = True
        user.is_staff = True
        user.save()
        
        if created:
            print("Admin created: user='admin', pass='admin12345'")
        else:
            print("Admin updated: password is now 'admin12345'")
            
    except Exception as e:
        print(f"WSGI Startup Error: {e}")

# Запускаем скрипт настройки
setup_app()

app = application