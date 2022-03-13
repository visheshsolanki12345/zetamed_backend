from django.urls import path
from micro_api import views

urlpatterns = [
    path('get-county-state-city/', views.country_state_city, name='get-county-state-city'),
]