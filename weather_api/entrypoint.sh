#!/bin/bash

# Выполнение миграций
python manage.py migrate

# Создание суперпользователя (если не существует)
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="${DJANGO_SUPERUSER_USERNAME}").exists():
    User.objects.create_superuser(
        "${DJANGO_SUPERUSER_USERNAME}",
        "${DJANGO_SUPERUSER_EMAIL}",
        "${DJANGO_SUPERUSER_PASSWORD}"
    )
END

# Запуск Gunicorn
exec gunicorn weather_project.wsgi:application --bind 0.0.0.0:8000
