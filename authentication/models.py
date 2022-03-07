from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User
import os
from django.conf import settings
from numpy import blackman
# Create your models here.

def user_directory_path_main(instance, filename):
    profile_pic_name = f'profile_picture/{instance.user.username}/{filename}'
    full_path = os.path.join(settings.MEDIA_ROOT, profile_pic_name)
    if os.path.exists(full_path):
        os.remove(full_path)
    return profile_pic_name

class OtpVerify(models.Model):
    mobileNo = models.IntegerField(null=False, blank=False)
    isOtp = models.IntegerField(null=False, blank=False)
    msgStatus = models.BooleanField(null=True, blank=True)
    msgId = models.CharField(null=True, blank=True, max_length=500)
    isVerify = models.BooleanField(default=False)
    maxTry = models.IntegerField(default=1, null=True, blank=True)
    isBlockNumber = models.BooleanField(default=False)
    createAt = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobileNo = models.IntegerField(null=False, blank=False)
    iAm = models.CharField(null=True, blank=True, max_length=500)
    speciality = models.CharField(null=True, blank=True, max_length=500)
    clinicName = models.CharField(null=True, blank=True, max_length=500)
    profileImage = models.ImageField(upload_to = 'profile-images', null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

