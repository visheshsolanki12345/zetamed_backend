
from django.urls import path, include
from patient import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

# User Url
router.register('get-patient', views.AllPatientViewSet, basename="get-patient")
router.register('get-patient-group', views.PatientGroupViewSet, basename="get-patient-group")

urlpatterns = [
    path('', include(router.urls)),
]

