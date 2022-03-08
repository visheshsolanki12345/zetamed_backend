from django.contrib import admin
from .models import PatientDetails, IsStaffCategory
# Register your models here.

@admin.register(PatientDetails)
class PatientDetailsAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'name', 'age', 'gender', 'mobileNo', 'email',
        'city', 'state', 'country', 'zipcode', 'problem', 'problemDescription',
        'patientImage', 'createAt',
    ]

@admin.register(IsStaffCategory)
class IsStaffCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_users', 'isStaff']
    