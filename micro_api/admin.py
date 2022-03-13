from django.contrib import admin
from .models import Country, State, City
# Register your models here.

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin): 
    list_display = ['id', 'country', 'get_state']

@admin.register(State)
class StateAdmin(admin.ModelAdmin): 
    list_display = ['id', 'state', 'get_city'] 

@admin.register(City)
class CityAdmin(admin.ModelAdmin): 
    list_display = ['id', 'city']