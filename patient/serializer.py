from rest_framework import serializers

from .models import (
    PatientDetails, PatientByUser,
    PatientGroup, Appointment, AppointmentByUser
)
import time
from datetime import datetime


class PatientDetailsSerializer(serializers.ModelSerializer):
    createAt = serializers.DateTimeField(format="%B %d, %Y, %I:%M%p")
    class Meta:
        model = PatientDetails
        fields = [
            'id', 'age', 'name', 'gender', 'mobileNo', 'email',
            'problem', 'createAt',
        ]


class PatientGroupSerializer(serializers.ModelSerializer):
    createAt = serializers.DateTimeField(format="%B %d, %Y, %I:%M%p")
    class Meta:
        model = PatientGroup
        fields = [
            'id', 'disease', 'diseaseDiscription', 'createAt'
        ]


class PatientInfoSerializer(serializers.ModelSerializer):
    createAt = serializers.DateTimeField(format="%B %d, %Y, %I:%M%p")
    age = serializers.DateField(format="%B %d, %Y")
    class Meta:
        model = PatientDetails
        fields = [
            'id', 'age', 'name', 'gender', 'whichProof', 'proofId', 'mobileNo', 'email',
            'city', 'state', 'country', 'zipcode', 'problem', 'problemDescription',
            'patientImage', 'patientGroupId', 'createAt',
        ]


class PatientByUserSerializer(serializers.ModelSerializer):
    patient = PatientDetailsSerializer(many=True, read_only=True)
    class Meta:
        model = PatientByUser
        fields = ['id', 'patient']


class AppointmentSerializer(serializers.ModelSerializer):
    # patient = PatientDetailsSerializer(many=False, read_only=True)
    # startDate = serializers.DateTimeField(format="%Y %#m, %#d, %#H, %#M")
    # endDate = serializers.DateTimeField(format="%Y %#m, %#d, %#H, %#M")
    createAt = serializers.DateTimeField(format="%B %d, %Y, %I:%M%p")
    class Meta:
        model = Appointment
        fields = [
            'id', 'patient', 'patientName', 'title', 'startDate', 'endDate',
            'isAppointmentDone', 'createAt'
        ]


class AppointmentByUserSerializer(serializers.ModelSerializer):
    appointment = AppointmentSerializer(many=True, read_only=True)
    class Meta:
        model = AppointmentByUser
        fields = [
            'id', 'user', 'appointment'
        ]
