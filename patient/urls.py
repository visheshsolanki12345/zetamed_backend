
from django.urls import path, include
from patient import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

# User Url
router.register('get-patient', views.AllPatientViewSet, basename="get-patient")
router.register('get-patient-group', views.PatientGroupViewSet, basename="get-patient-group")
router.register('get-patient-appointment', views.PatientAppointmentViewSet, basename="get-patient-appointment")
router.register('add-prescription', views.PrescriptionViewSet, basename="add-prescription")

urlpatterns = [
    path('', include(router.urls)),
    path('search-patient/', views.patient_search, name='search-patient'),
    path('patient-info/<str:pk>/', views.patient_info_print, name='patient-info'),
    path('done-appontment/', views.get_done_appointment, name='done-appontment'),
]

