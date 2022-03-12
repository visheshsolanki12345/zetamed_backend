from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.

class OtpVerify(models.Model):
    mobileNo = models.IntegerField(null=False, blank=False)
    isOtp = models.IntegerField(null=False, blank=False)
    msgStatus = models.BooleanField(null=True, blank=True)
    msgId = models.CharField(null=True, blank=True, max_length=500)
    isVerify = models.BooleanField(default=False)
    maxTry = models.IntegerField(default=1, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    createAt = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4, editable = False)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    mobileNo = models.IntegerField(null=False, blank=False)
    iAm = models.CharField(null=True, blank=True, max_length=500)
    speciality = models.CharField(null=True, blank=True, max_length=500)
    clinicName = models.CharField(null=True, blank=True, max_length=500)
    profileImage = models.ImageField(null=True, blank=True,upload_to='profile-images', default="profile-images/Profile.png")
    createdAt = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.id)


