import os
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo.settings')

application = get_wsgi_application()

# Скрипт автоматизации при запуске
try:
    # 1. Создаем таблицы
    call_command('migrate', interactive=False)
    
    # 2. Собираем статику
    call_command('collectstatic', '--noinput')

    # 3. Создаем админа, если его еще нет
    User = get_user_model()
    # Замени 'admin' и '12345' на свои логин и пароль
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', '12345')
        print("Admin created: login 'admin', pass '12345'")
    else:
        print("Admin already exists")

except Exception as e:
    print(f"Startup script error: {e}")

app = application