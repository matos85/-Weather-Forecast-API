import requests
from datetime import datetime
from django.conf import settings

def get_current_weather(city):
    api_key = settings.OPENWEATHERMAP_API_KEY
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    return {
        "temperature": data["main"]["temp"],
        "local_time": datetime.fromtimestamp(data["dt"] + data["timezone"]).strftime("%H:%M"),
    }

def get_forecast(city, date):
    api_key = settings.OPENWEATHERMAP_API_KEY
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    target_date = date.strftime("%Y-%m-%d")
    for forecast in data["list"]:
        forecast_date = datetime.fromtimestamp(forecast["dt"]).strftime("%Y-%m-%d")
        if forecast_date == target_date:
            return {
                "min_temperature": forecast["main"]["temp_min"],
                "max_temperature": forecast["main"]["temp_max"],
            }
    return None