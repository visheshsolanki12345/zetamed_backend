from email.policy import default
from django.db import models
from django.contrib.auth.models import User
import os
from django.conf import settings
import uuid
# Create your models here.

def user_directory_path_main(instance, filename):
    profile_pic_name = f'patient-images/{instance.user.username}/{filename}'
    full_path = os.path.join(settings.MEDIA_ROOT, profile_pic_name)
    if os.path.exists(full_path):
        os.remove(full_path)
    return profile_pic_name


class PatientDetails(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4, editable = False)
    name = models.CharField(null=True, blank=True, max_length=500)
    age = models.DateField(null=True, blank=True)
    gender = models.CharField(null=True, blank=True, max_length=500)
    whichProof = models.CharField(null=True, blank=True, max_length=500)
    proofId = models.CharField(null=True, blank=True, max_length=500)
    mobileNo = models.IntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    city = models.CharField(null=True, blank=True, max_length=400)
    state = models.CharField(null=True, blank=True, max_length=400)
    country = models.CharField(null=True, blank=True, max_length=400)
    zipcode = models.IntegerField(null=True, blank=True)
    problem = models.CharField(max_length=500, null=True, blank=True)
    problemDescription = models.TextField(null=True, blank=True)
    patientImage = models.ImageField(upload_to = user_directory_path_main, null=True, blank=True, default = 'patient-images/avtar.png')
    createAt = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.id)


class PatientByUser(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4, editable = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    patient = models.ManyToManyField(PatientDetails, related_name='patient', blank=True)

    def get_patients(self):
        return ",".join([str(p) for p in self.patient.all()])

    def __str__(self):
        return str(self.id)
    


class IsStaffCategory(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4, editable = False)
    user = models.ManyToManyField(User)
    isStaff = models.CharField(null=True, blank=True, max_length=500)
    def get_users(self):
        return ",".join([str(p) for p in self.user.all()])

    def __str__(self):
        return str(self.id)

# class StaffDetails(models.Model):
#     user = models.ManyToManyField(User)
#     name = models.CharField(null=True, blank=True, max_length=500)
#     degree = models.CharField(null=True, blank=True, max_length=500)
#     mobile = models.CharField(null=True, blank=True, max_length=500)
#     email = models.CharField(null=True, blank=True, max_length=500)
#     email = models.CharField(null=True, blank=True, max_length=500)