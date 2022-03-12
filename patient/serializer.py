from rest_framework import serializers
from .models import (
    PatientDetails, PatientByUser, 
    PatientGroup,
)

class PatientDetailsSerializer(serializers.ModelSerializer):  
    createAt = serializers.DateTimeField(format = "%B %d, %Y, %I:%M%p")  
    class Meta:
        model = PatientDetails
        fields = [
            'id', 'age', 'name', 'gender', 'mobileNo', 'email',
            'problem','createAt', 'patientImage',
        ]

class PatientGroupSerializer(serializers.ModelSerializer):  
    createAt = serializers.DateTimeField(format = "%B %d, %Y, %I:%M%p")  
    class Meta:
        model = PatientGroup
        fields = [
            'id', 'disease', 'diseaseDiscription', 'createAt'
        ]

# class PatientInfoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PatientDetails
#         fields = [
#             'id', 'age', 'name', 'gender', 'whichProof', 'proofId', 'mobileNo', 'email',
#             'city', 'state', 'country', 'zipcode', 'problem', 'problemDescription',
#             'patientImage', 'createAt',
#         ]

class PatientByUserSerializer(serializers.ModelSerializer):
    patient = PatientDetailsSerializer(many=True, read_only=True)
    class Meta:
        model = PatientByUser
        fields = ['patient']
