
from django.urls import path, include
from patient import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

# User Url
router.register('get-patient', views.AllPatientViewSet, basename="get-patient")

urlpatterns = [
    path('', include(router.urls)),
]

