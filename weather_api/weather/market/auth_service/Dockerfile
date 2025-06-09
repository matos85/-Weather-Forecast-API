FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Установка postgresql-client для pg_isready
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*
COPY . .

ENV ENVIRONMENT=production
EXPOSE 8000

# Ожидание PostgreSQL с тайм-аутом 30 секунд, затем запуск миграций и приложения
CMD ["sh", "-c", "for i in $(seq 30); do if pg_isready -h db -p 5432 -U user; then break; fi; echo 'Waiting for PostgreSQL... ($i/30)'; sleep 1; done && if ! pg_isready -h db -p 5432 -U user; then echo 'Timeout waiting for PostgreSQL'; exit 1; fi && alembic upgrade head && gunicorn -c gunicorn_conf.py main:app"]