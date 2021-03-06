from rest_framework import status
from threading import Thread
from . import signals
from .models import (
    PatientDetails, PatientByUser,
     Appointment, AppointmentByUser,
    Prescription, PrescriptionByUser
)
from .serializer import (
    PatientDetailsSerializer, 
    PatientInfoSerializer, AppointmentSerializer,
)
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
import time
import re
from django.core.cache import cache


# Create your views here.
class AllPatientGetData:
    def __init__(self):
        self.context = ''
        Thread.__init__(self)

    def all_data_thread(self, request):
        # start_time = time.time()
        query_filter = request.query_params.get('query')
        obj = PatientByUser.objects.get(user = request.user)
        patient = ''
        image_list = []

        if query_filter == None:
            query_filter = ''

        if query_filter != '':
            patient = obj.patient.filter(
                Q(name__icontains=query_filter) 
                | Q(mobileNo__icontains=query_filter) 
                | Q(proofId__icontains=query_filter)
                | Q(email__icontains=query_filter) 
                ).values(
                    'id', 'name', 'age', 'gender', 'mobileNo', 
                    'email', 'problem', 'createAt', "patientImage"
                ).order_by('-createAt')
        else:
            try:
                # if cache.get(str(request.user.id)):
                #     patient = cache.get(str(request.user.id))
                # else:
                    patient = obj.patient.all().values(
                        'id', 'name', 'age', 'gender', 'mobileNo', 
                        'email', 'problem', 'createAt', "patientImage"
                    ).order_by('-createAt')
                    cache.set(str(request.user.id), patient)
            except:
                self.context = {'status' : status.HTTP_400_BAD_REQUEST, "details" : "data not found"}

        page = request.query_params.get('page')
        paginator = Paginator(patient, 2)
        total_patient_count = patient.__len__()
        try:
            patient = paginator.page(page)
        except PageNotAnInteger:
            patient = paginator.page(1)
        except EmptyPage:
            patient = paginator.page(paginator.num_pages)

        if page == None:
            page = 1
        for i in patient:
            for i in patient:
                image_list.append(str(i['patientImage']))  
        page = int(page)

        page = int(page)
        serializer = PatientDetailsSerializer(patient, many=True)
        self.context = {
            'status' : status.HTTP_202_ACCEPTED, 
            'data' : serializer.data, 'page': page, 
            'pages': paginator.num_pages,
            "images" : image_list,
            'patientCount' : total_patient_count,
            'query': query_filter, 
        }
        # print("--- %s seconds ---" % (time.time() - start_time))
        return
    
    def single_data_thread(self, request, pk):
        obj = PatientDetails.objects.filter(id = pk)
        serializer = PatientInfoSerializer(obj, many=True)
        self.context = {
            'status': status.HTTP_202_ACCEPTED, 
            'data': serializer.data,
        }
        return
            

    def create_data_thread(self, request):
        data = request.data
        try:
            obj = PatientDetails(
                name = data['name'],
                age = data['age'],
                gender = data['gender'],
                whichProof = data['whichProof'],
                proofId = data['proofId'],
                mobileNo = data['mobileNo'],
                email = data['email'],
                address = data['address'],
                problem = data['problem'],
                problemDescription = data['problemDescription'],
            )
            obj.save()
            signals.patient_profile_data.send(sender=None, request=request, obj = obj)
            try:
                patien_data = PatientByUser.objects.get(user = request.user)
                patien_data.patient.add(obj)
                patien_data.save()
            except:
                patien_data = PatientByUser(user = request.user)
                patien_data.patient.add(obj)
                patien_data.save()
            cache.delete(str(request.user.id))
            self.context = {'status' : status.HTTP_201_CREATED, 'details' : 'Patient record successfully added!'}
        except:
            self.context = {'status' : status.HTTP_204_NO_CONTENT, 'details' : 'Patient not added!'}
        return



    def update_data_thread(self, request, pk):
        data = request.data
        try:
            PatientDetails.objects.filter(
                id = pk,
            ).update(
                name = data['name'],
                age = data['age'],
                gender = data['gender'],
                whichProof = data['whichProof'],
                proofId = data['proofId'],
                mobileNo = data['mobileNo'],
                email = data['email'],
                address = data['address'],
                problem = data['problem'],
                problemDescription = data['problemDescription'],
            )

            obj = PatientDetails.objects.get(id = pk)
            signals.patient_profile_data.send(sender=None, request=request, obj = obj)
            cache.delete(str(request.user.id))
            self.context = {'status' : status.HTTP_201_CREATED, 'details' : 'Patient record successfully Update!'}
        except:
            self.context = {'status' : status.HTTP_204_NO_CONTENT, 'details' : 'Patient not Update!'}
        return

    
    def delete_data_thread(self, request, pk):
        PatientDetails.objects.filter(id = pk).delete()
        self.context = {'status' : status.HTTP_200_OK, 'details' : 'Patient Successfully Deleted.'}
        cache.delete(str(request.user.id))
        return


class PatientAppointmentThread:
    def __init__(self):
        Thread.__init__(self,)
        self.context = ''
    
    def all_data_thread(self, request):
        try:
            obj = AppointmentByUser.objects.get(user = request.user)
            appointment_data = obj.appointment.all()
            serializer = AppointmentSerializer(appointment_data, many=True)
            self.context = {"status": status.HTTP_200_OK, "data": serializer.data }
        except:
            self.context = {"status": status.HTTP_404_NOT_FOUND, "details": "data not found" }


    def create_data_thread(self, request):
        try:
            data = request.data
            patient_obj = PatientDetails.objects.get(id = data['id'])
            obj = Appointment(
                patient = patient_obj,
                patientName = patient_obj.problem,
                title = patient_obj.name,
                startDate = data['startDate'],
                endDate = data['endDate'],
            )
            obj.save()
            try:
                appointment_user_by = AppointmentByUser.objects.get(user = request.user)
                appointment_user_by.appointment.add(obj)
                appointment_user_by.save()
            except:
                appointment_user_by = AppointmentByUser(user = request.user)
                appointment_user_by.appointment.add(obj)
                appointment_user_by.save()

            self.context = {'status' : status.HTTP_201_CREATED, 'details' : 'Patient Appointment successfully added!'}
        except:
            self.context = {'status' : status.HTTP_204_NO_CONTENT, 'details' : 'Patient not added!'}
        return

    def update_data_thread(self, request, pk):
        data = request.data
        try:
            obj = Appointment.objects.get(id = pk)
            if data['check'] == '1':
                obj.patientName = data['patientName']
                obj.startDate = data['startDate']
                obj.endDate = data['endDate']
            elif data['check'] == '2':
                obj.isAppointmentDone = data['conformation']
            obj.save()
            self.context = {'status' : status.HTTP_202_ACCEPTED, 'details' : 'Patient appointment successfully Updated!'}
        except:
            self.context = {'status' : status.HTTP_304_NOT_MODIFIED, 'details' : 'Patient appointment not Updated!'}
        return
    
    def delete_data_thread(self, pk):
        Appointment.objects.filter(id = pk).delete()
        self.context = {'status' : status.HTTP_200_OK, 'details' : 'Patient Appointment Successfully Deleted.'}
        return


class PrescriptionThread:
    def __init__(self):
        Thread.__init__(self,)
        self.context = ''
    
    # def all_data_thread(self, request):
    #     try:
    #         obj = AppointmentByUser.objects.get(user = request.user)
    #         appointment_data = obj.appointment.all()
    #         serializer = AppointmentSerializer(appointment_data, many=True)
    #         self.context = {"status": status.HTTP_200_OK, "data": serializer.data }
    #     except:
    #         self.context = {"status": status.HTTP_404_NOT_FOUND, "details": "data not found" }


    def create_data_thread(self, request):
        try:
            data = request.data
            appointment_obj = Appointment.objects.get(id=data['appointmentId'])
            appointment_obj.isAppointmentDone = "Done"
            appointment_obj.save()
            obj = Prescription(
                appointment=appointment_obj,
                prescriptionDetails=data['jsonData'],
            )
            obj.save()
            try:
                obj_user_by = PrescriptionByUser.objects.get(user = request.user)
                obj_user_by.prescription.add(obj)
                obj_user_by.save()
            except:
                obj_user_by = PrescriptionByUser.objects.create(
                    user = request.user
                )
                obj_user_by.prescription.add(obj)
                obj_user_by.save()
            self.context = {'status' : status.HTTP_201_CREATED, 'details' : 'Prescription successfully added!'}
        except:
            self.context = {'status' : status.HTTP_204_NO_CONTENT, 'details' : 'Prescription not added!'}
        return
        

    # def update_data_thread(self, request, pk):
    #     data = request.data
    #     try:
    #         obj = Appointment.objects.get(id = pk)
    #         if data['check'] == '1':
    #             obj.patientName = data['patientName']
    #             obj.startDate = data['startDate']
    #             obj.endDate = data['endDate']
    #         elif data['check'] == '2':
    #             obj.isAppointmentDone = data['conformation']
    #         obj.save()
    #         self.context = {'status' : status.HTTP_202_ACCEPTED, 'details' : 'Patient appointment successfully Updated!'}
    #     except:
    #         self.context = {'status' : status.HTTP_304_NOT_MODIFIED, 'details' : 'Patient appointment not Updated!'}
    #     return
    
    # def delete_data_thread(self, pk):
    #     Appointment.objects.filter(id = pk).delete()
    #     self.context = {'status' : status.HTTP_200_OK, 'details' : 'Patient Appointment Successfully Deleted.'}
    #     return