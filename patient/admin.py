from django.contrib import admin
from .models import (
    PatientDetails, IsStaffCategory, PatientByUser, PatientGroup,
    PatientGroupByUser, 
)
# Register your models here.

@admin.register(PatientDetails)
class PatientDetailsAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'age', 'gender', 'whichProof', 'proofId', 'mobileNo', 'email',
        'city', 'state', 'country', 'zipcode', 'problem', 'problemDescription',
        'patientImage', 'createAt'
    ]

@admin.register(PatientGroup)
class PatientGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'disease', 'diseaseDiscription', 'createAt']

@admin.register(PatientGroupByUser)
class PatientGroupByUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'get_patientGroup']

# @admin.register(IsStaffCategory)
# class IsStaffCategoryAdmin(admin.ModelAdmin):
#     list_display = ['id', 'get_users', 'isStaff']
    
@admin.register(PatientByUser)
class PatientByUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'get_patients', 'patientGroup']


    