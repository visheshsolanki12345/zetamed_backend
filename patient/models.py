from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class PatientDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(null=True, blank=True, max_length=500)
    age = models.DateField(null=True, blank=True)
    gender = models.CharField(null=True, blank=True, max_length=500)
    mobileNo = models.IntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    city = models.CharField(null=True, blank=True, max_length=400)
    state = models.CharField(null=True, blank=True, max_length=400)
    country = models.CharField(null=True, blank=True, max_length=400)
    zipcode = models.IntegerField(null=True, blank=True)
    problem = models.CharField(max_length=500, null=True, blank=True)
    problemDescription = models.TextField(null=True, blank=True)
    patientImage = models.ImageField(upload_to = 'patient-images', null=True, blank=True)
    createAt = models.DateTimeField(auto_now_add=True)

