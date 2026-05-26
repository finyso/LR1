#!/bin/bash

# Ждем готовности базы данных
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Database ready!"

# Применяем миграции
echo "Applying migrations..."
python manage.py migrate

# Собираем статику
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Создаем суперпользователя (если нужно)
echo "Creating superuser..."
python manage.py shell -c "
from django.contrib.auth.models import User;
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
"

# Запускаем сервер
echo "Starting server..."
exec "$@"