from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from threading import Thread
from rest_framework_simplejwt.authentication import JWTAuthentication


from .models import AppointmentByUser, PatientDetails
from .serializer import PatientDetailsSerializer

from patient.models import Appointment, Prescription
from . import thread_views
import time
import json

class AllPatientViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def list(self, request):
        class_obj = thread_views.AllPatientGetData()
        patient_list = Thread(
            target=class_obj.all_data_thread, args=(request,))
        patient_list.start()
        patient_list.join()
        return Response(class_obj.context)

    def retrieve(self, request, pk=None):
        class_obj = thread_views.AllPatientGetData()
        patient_ret = Thread(
            target=class_obj.single_data_thread, args=(request, pk))
        patient_ret.start()
        patient_ret.join()
        return Response(class_obj.context)

    def create(self, request, pk=None):
        class_obj = thread_views.AllPatientGetData()
        patient_create = Thread(
            target=class_obj.create_data_thread, args=(request,))
        patient_create.start()
        patient_create.join()
        return Response(class_obj.context)

    def update(self, request, pk=None):
        class_obj = thread_views.AllPatientGetData()
        patient_create = Thread(
            target=class_obj.update_data_thread, args=(request, pk))
        patient_create.start()
        patient_create.join()
        return Response(class_obj.context)

    def destroy(self, request, pk=None):
        class_obj = thread_views.AllPatientGetData()
        patient_ret = Thread(
            target=class_obj.delete_data_thread, args=(request, pk))
        patient_ret.start()
        patient_ret.join()
        return Response(class_obj.context)


class PatientGroupViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def list(self, request):
        class_obj = thread_views.AllPatientGroupGetData()
        patient_gr_list = Thread(
            target=class_obj.all_data_thread, args=(request,))
        patient_gr_list.start()
        patient_gr_list.join()
        return Response(class_obj.context)

    def retrieve(self, request, pk=None):
        class_obj = thread_views.AllPatientGroupGetData()
        patient_group_list = Thread(
            target=class_obj.single_data_thread, args=(pk,))
        patient_group_list.start()
        patient_group_list.join()
        return Response(class_obj.context)

    def create(self, request, pk=None):
        class_obj = thread_views.AllPatientGroupGetData()
        patient_group_create = Thread(
            target=class_obj.create_data_thread, args=(request,))
        patient_group_create.start()
        patient_group_create.join()
        return Response(class_obj.context)

    def update(self, request, pk=None):
        class_obj = thread_views.AllPatientGroupGetData()
        patient_group_update = Thread(
            target=class_obj.update_data_thread, args=(request, pk))
        patient_group_update.start()
        patient_group_update.join()
        return Response(class_obj.context)

    def destroy(self, request, pk=None):
        class_obj = thread_views.AllPatientGroupGetData()
        patient_ret = Thread(target=class_obj.delete_data_thread, args=(pk,))
        patient_ret.start()
        patient_ret.join()
        return Response(class_obj.context)


class PatientAppointmentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def list(self, request):
        class_obj = thread_views.PatientAppointmentThread()
        patient_appo_list = Thread(
            target=class_obj.all_data_thread, args=(request,))
        patient_appo_list.start()
        patient_appo_list.join()
        return Response(class_obj.context)

    def create(self, request):
        class_obj = thread_views.PatientAppointmentThread()
        patient_appo_list = Thread(
            target=class_obj.create_data_thread, args=(request,))
        patient_appo_list.start()
        patient_appo_list.join()
        return Response(class_obj.context)

    def update(self, request, pk=None):
        class_obj = thread_views.PatientAppointmentThread()
        patient_group_update = Thread(
            target=class_obj.update_data_thread, args=(request, pk))
        patient_group_update.start()
        patient_group_update.join()
        return Response(class_obj.context)

    def destroy(self, request, pk=None):
        class_obj = thread_views.PatientAppointmentThread()
        patient_appo_list = Thread(
            target=class_obj.delete_data_thread, args=(pk,))
        patient_appo_list.start()
        patient_appo_list.join()
        return Response(class_obj.context)



class PrescriptionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self, request):
        class_obj = thread_views.PrescriptionThread()
        prescription_tr = Thread(target = class_obj.create_data_thread, args=(request,))
        prescription_tr.start()
        prescription_tr.join()
        return Response(class_obj.context)




@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def patient_search(request):
    obj = thread_views.PatientByUser.objects.get(user=request.user)
    patient = obj.patient.all().values('id', 'name', 'mobileNo').order_by('-createAt')
    return Response(patient)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def patient_info_print(request, pk):
    obj = PatientDetails.objects.filter(id = pk)
    serializer = PatientDetailsSerializer(obj, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_done_appointment(request):
    obj = AppointmentByUser.objects.get(user = request.user)
    appoitment = obj.appointment.filter(isAppointmentDone = "Done").values("id", "patient", "title").order_by("createAt")
    context = {}
    for i in appoitment:
        context["id"] = str(i["id"])
        context["patientId"] = str(i["patient"])
        context["patientName"] = i["title"]
    return Response(context)


def test(request):
    pass

