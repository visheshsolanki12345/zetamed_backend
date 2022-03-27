from django.contrib import admin
from .models import (
    PatientDetails, PatientByUser,
     Appointment, AppointmentByUser,
    Prescription, PrescriptionByUser, 
)
# Register your models here.

@admin.register(PatientDetails)
class PatientDetailsAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'age', 'gender', 'whichProof', 'proofId', 'mobileNo', 'email',
        'address','problem', 'problemDescription',
        'patientImage', 'createAt'
    ]
@admin.register(PatientByUser)
class PatientByUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'get_patients']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'patient', 'patientName', 'title', 'startDate', 'endDate', 
        'isAppointmentDone', 'createAt'
        ]

@admin.register(AppointmentByUser)
class AppointmentByUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'get_appointments']


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'prescriptionDetails', 'status', 'createAt' 
    ]

@admin.register(PrescriptionByUser)
class PrescriptionByUserAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'get_prescriptions'
    ]




    