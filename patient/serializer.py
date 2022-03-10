from asyncore import read
from rest_framework import serializers
from .models import PatientDetails, PatientByUser

class PatientDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDetails
        fields = [
            'id', 'age', 'name', 'gender', 'whichProof', 'proofId', 'mobileNo', 'email',
            'city', 'state', 'country', 'zipcode', 'problem', 'problemDescription',
            'patientImage', 'createAt',
        ]

class PatientByUserSerializer(serializers.ModelSerializer):
    patient = PatientDetailsSerializer(many=True, read_only=True)
    class Meta:
        model = PatientByUser
        fields = ['patient']
