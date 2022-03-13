from django.db import models
from django.contrib.auth.models import User
import os
from django.conf import settings
import uuid
import jsonfield
from django_mysql.models import ListCharField
from django.db.models import CharField, Model
from django_mysql.models import ListF

# Create your models here.

def user_directory_path_main(instance, filename):
    pass
    # profile_pic_name = f'{instance.user.username}/{filename}'
    # full_path = os.path.join(settings.MEDIA_ROOT, profile_pic_name)
    # if os.path.exists(full_path):
    #     os.remove(full_path)
    # return profile_pic_name

class PatientGroup(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4, editable = False)
    disease = models.CharField(null=True, blank=True, max_length=500)
    diseaseDiscription = models.TextField(null=True, blank=True)
    createAt = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.id)

class PatientGroupByUser(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4, editable = False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    patientGroup = models.ManyToManyField(PatientGroup, blank=True)
    def get_patientGroup(self):
        return ",".join([str(p) for p in self.patientGroup.all()])

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
    patientGroupId = models.CharField(null=True, blank=True, max_length=500)
    patientImage = models.ImageField(upload_to = user_directory_path_main('a', 'b'), default = 'patient-images/avtar.png', null=True, blank=True)
    createAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class PatientByUser(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4, editable = False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    patient = models.ManyToManyField(PatientDetails, blank=True)
    patientGroup = jsonfield.JSONField()

    # def save(self, *args, **kwargs):
    #     context = {}
    #     self.patientGroup 
    #     super(PatientByUser, self).save(*args, **kwargs)

    def get_patients(self):
        return ",".join([str(p) for p in self.patient.all()])
    
    # def get_patientGroup(self):
    #     return ",".join([str(p) for p in self.patientGroup.all()])

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