from rest_framework import serializers
from .models import Country, State, City

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['city']

class StateSerializer(serializers.ModelSerializer):
    city = CitySerializer(many=True, read_only=True)
    class Meta:
        model = State
        fields = ['state', 'city']

class CountrySerializer(serializers.ModelSerializer):
    state = StateSerializer(many=True, read_only=True)
    class Meta:
        model = Country
        fields = ['country', 'state']

