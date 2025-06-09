from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CurrentWeatherSerializer, ForecastSerializer, ForecastOverrideSerializer
from .models import ForecastOverride
from .services import get_current_weather, get_forecast
from datetime import datetime


class CurrentWeatherView(APIView):
    def get(self, request):
        city = request.query_params.get("city")
        if not city:
            return Response({"error": "Параметр 'city' обязателен."}, status=status.HTTP_400_BAD_REQUEST)

        weather_data = get_current_weather(city)
        if not weather_data:
            return Response({"error": "Город не найден или ошибка внешнего API."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CurrentWeatherSerializer(weather_data)
        return Response(serializer.data)


class ForecastView(APIView):
    def get(self, request):
        city = request.query_params.get("city")
        date_str = request.query_params.get("date")

        if not city or not date_str:
            return Response({"error": "Параметры 'city' и 'date' обязательны."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            date = datetime.strptime(date_str, "%d.%m.%Y").date()
        except ValueError:
            return Response({"error": "Неверный формат даты. Используйте 'dd.MM.yyyy'."},
                            status=status.HTTP_400_BAD_REQUEST)

        override = ForecastOverride.objects.filter(city=city, date=date).first()
        if override:
            serializer = ForecastSerializer({
                "min_temperature": override.min_temperature,
                "max_temperature": override.max_temperature,
            })
            return Response(serializer.data)

        forecast_data = get_forecast(city, date)
        if not forecast_data:
            return Response({"error": "Прогноз для указанной даты недоступен или город не найден."},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = ForecastSerializer(forecast_data)
        return Response(serializer.data)

    def post(self, request):
        serializer = ForecastOverrideSerializer(data=request.data)
        if serializer.is_valid():
            city = serializer.validated_data["city"]
            date = serializer.validated_data["date"]
            ForecastOverride.objects.update_or_create(
                city=city, date=date,
                defaults={
                    "min_temperature": serializer.validated_data["min_temperature"],
                    "max_temperature": serializer.validated_data["max_temperature"],
                }
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)