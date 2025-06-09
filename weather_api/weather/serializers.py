from rest_framework import serializers
from .models import ForecastOverride
from datetime import datetime, timedelta


class CurrentWeatherSerializer(serializers.Serializer):
    temperature = serializers.FloatField()
    local_time = serializers.CharField(max_length=5)


class ForecastSerializer(serializers.Serializer):
    min_temperature = serializers.FloatField()
    max_temperature = serializers.FloatField()


class ForecastOverrideSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%d.%m.%Y", input_formats=["%d.%m.%Y"])

    class Meta:
        model = ForecastOverride
        fields = ["city", "date", "min_temperature", "max_temperature"]
        extra_kwargs = {
            "city": {"required": True},
            "date": {"required": True},
            "min_temperature": {"required": True},
            "max_temperature": {"required": True},
        }

    def validate(self, data):
        today = datetime.now().date()
        max_date = today + timedelta(days=10)

        # Проверка даты
        if data["date"] < today:
            raise serializers.ValidationError({"date": "Дата не может быть в прошлом."})
        if data["date"] > max_date:
            raise serializers.ValidationError({"date": "Дата не может быть позже 10 дней от текущей даты."})

        # Проверка температур
        if data["min_temperature"] > data["max_temperature"]:
            raise serializers.ValidationError(
                {"min_temperature": "Минимальная температура не может быть больше максимальной."})

        return data