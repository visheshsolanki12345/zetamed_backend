from django.contrib import admin
from .models import (
    PatientDetails, PatientByUser, PatientGroup,
    PatientGroupByUser, Appointment, AppointmentByUser
)
# Register your models here.

@admin.register(PatientDetails)
class PatientDetailsAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'age', 'gender', 'whichProof', 'proofId', 'mobileNo', 'email',
        'city', 'state', 'country', 'zipcode', 'problem', 'problemDescription',
        'patientImage', 'patientGroupId', 'createAt'
    ]
@admin.register(PatientByUser)
class PatientByUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'get_patients']



@admin.register(PatientGroup)
class PatientGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'disease', 'diseaseDiscription', 'createAt']

@admin.register(PatientGroupByUser)
class PatientGroupByUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'get_patientGroup']



@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'patient', 'patientName', 'title', 'startDate', 'endDate', 
        'isAppointmentDone', 'createAt'
        ]

@admin.register(AppointmentByUser)
class AppointmentByUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'get_appointments']
    




    