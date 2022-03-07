from rest_framework import serializers
from .models import PatientDetails

class PatientDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDetails
        fields = [
            'id', 'user', 'age', 'name', 'gender', 'mobileNo', 'email',
            'city', 'state', 'country', 'zipcode', 'problem', 'problemDescription',
            'patientImage', 'createAt',
        ]
