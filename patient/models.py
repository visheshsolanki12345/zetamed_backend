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


class PatientDetails(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4, editable = False)
    name = models.CharField(null=True, blank=True, max_length=500)
    age = models.DateField(null=True, blank=True)
    gender = models.CharField(null=True, blank=True, max_length=500)
    whichProof = models.CharField(null=True, blank=True, max_length=500)
    proofId = models.CharField(null=True, blank=True, max_length=500)
    mobileNo = models.IntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    problem = models.CharField(max_length=500, null=True, blank=True)
    problemDescription = models.TextField(null=True, blank=True)
    patientImage = models.ImageField(upload_to = user_directory_path_main('a', 'b'), default = 'patient-images/avtar.png', null=True, blank=True)
    createAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class PatientByUser(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4, editable = False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    patient = models.ManyToManyField(PatientDetails, blank=True)

    def get_patients(self):
        return ",".join([str(p) for p in self.patient.all()])
    
    def __str__(self):
        return str(self.user)
    

class Appointment(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4, editable = False)
    patient = models.ForeignKey(PatientDetails, on_delete=models.CASCADE, null=True, blank=True)
    patientName = models.CharField(max_length=400, null=True, blank=True)
    title = models.CharField(max_length=400, null=True, blank=True)
    startDate = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    endDate = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    isAppointmentDone = models.CharField(max_length=225, default='Panding', null=True, blank=True)
    createAt = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    def __str__(self):
        return str(f"{self.patient}")

class AppointmentByUser(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4, editable = False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    appointment = models.ManyToManyField(Appointment)
    def get_appointments(self):
        return ",".join([str(p) for p in self.appointment.all()])


class Prescription(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4, editable = False)
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True)
    prescriptionDetails = jsonfield.JSONField()
    status = models.CharField(max_length=225, default='approve', null=True, blank=True)
    createAt = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.appointment)


class PrescriptionByUser(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4, editable = False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    prescription = models.ManyToManyField(Prescription, blank=True)

    def get_prescriptions(self):
        return ",".join([str(p) for p in self.prescription.all()])
    
    def __str__(self):
        return str(self.user)