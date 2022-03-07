from django.contrib import admin
from .models import OtpVerify, Profile
# Register your models here.

@admin.register(OtpVerify)
class OtpVerifyAdmin(admin.ModelAdmin): 
    list_display = [
        'id', 'mobileNo', 'isOtp', 'msgStatus', 'msgId', 'isVerify', 
        'maxTry', 'isBlockNumber', 'createAt'
        ]

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin): 
    list_display = [
        'id', 'user', 'mobileNo', 'iAm', 'speciality', 'clinicName', 
        'profileImage', 'createdAt',
        ]