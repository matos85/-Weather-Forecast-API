# 🌤️ Weather Forecast API

REST API для получения текущей погоды и прогноза с возможностью ручного переопределения данных. Использует [OpenWeatherMap API](https://openweathermap.org/api).

---

## 🚀 Возможности

- Получение текущей температуры и локального времени по городу
- Прогноз (мин/макс температура) на заданную дату
- Ручное переопределение прогноза (POST-запрос)
- Хранение переопределённых данных в PostgreSQL
- Интеграция с внешним OpenWeatherMap API

---

## 🔧 Технологии

- Python 3.11
- Django 4.x
- Django REST Framework
- PostgreSQL 15
- Gunicorn
- Docker + Docker Compose

---

## ⚙️ Установка и запуск (Docker)

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/matos85/-Weather-Forecast-API
cd -Weather-Forecast-API/weather-api    
```



### 2. Соберите и запустите контейнеры

```bash
docker-compose up --build -d
```

### 3. Откройте приложение

```txt
http://<your_server_ip>:8002/
```

---

## 📌 Эндпоинты API

| Метод | URL                          | Назначение                       |
|-------|------------------------------|----------------------------------|
| GET   | `/api/weather/current?city=` | Текущая погода и локальное время |
| GET   | `/api/weather/forecast`      | Прогноз температуры на дату      |
| POST  | `/api/weather/forecast`      | Переопределение прогноза         |

---

## 🧪 Примеры запросов

### 🔹 1. Текущая погода:

**GET** `/api/weather/current?city=London`

**Пример ответа:**

```json
{
  "temperature": 22.1,
  "local_time": "16:45"
}
```

---

### 🔹 2. Прогноз погоды на дату:

**GET** `/api/weather/forecast?city=Москва&date=10.06.2025`

**Пример ответа:**

```json
{
  "city": "Москва",
  "date": "10.06.2025",
  "min_temperature": 16.3,
  "max_temperature": 24.1,
  "source": "api"
}
```

---

### 🔹 3. Переопределение прогноза:

**POST** `/api/weather/forecast`

**Пример тела запроса:**

```json
{
  "city": "Москва",
  "date": "10.06.2025",
  "min_temperature": 18.5,
  "max_temperature": 26.0
}
```

**Пример ответа:**

```json
{
  "city": "Москва",
  "date": "10.06.2025",
  "min_temperature": 18.5,
  "max_temperature": 26.0,
  "source": "override"
}
```

---


