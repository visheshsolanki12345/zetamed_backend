from html5lib import serialize
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from threading import Thread
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import (
    PatientDetails, PatientByUser
)
from .serializer import (
    PatientDetailsSerializer, PatientByUserSerializer
)
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import time

# Create your views here.
class AllPatientGetData:
    def __init__(self):
        self.context = ''
        Thread.__init__(self)

    def all_data_thread(self, request):
        # start_time = time.time()
        query_name = request.query_params.get('name')
        query_mobile = request.query_params.get('mobile')
        query_email = request.query_params.get('email')
        query_proofId = request.query_params.get('proofId')
        query_date = request.query_params.get('date')
        patient = ''
        if query_name == None:
            query_name = ''
        if query_mobile == None:
            query_mobile = ''
        if query_email == None:
            query_email = ''
        if query_proofId == None:
            query_proofId = ''
        if query_date == None:
            query_date = ''
        
        if query_name != '':
            obj_patient = PatientDetails.objects.filter(name__icontains=query_name).order_by('-createAt')
        elif query_mobile != '':
            obj_patient = PatientDetails.objects.filter(mobileNo__icontains=query_mobile).order_by('-createAt')
        elif query_email != '':
            obj_patient = PatientDetails.objects.filter(email__icontains=query_email).order_by('-createAt')
        elif query_proofId != '':
            obj_patient = PatientDetails.objects.filter(proofId__icontains=query_proofId).order_by('-createAt')
        try:
            id_list = []
            patient = []
            for i in obj_patient:
                id_list.append(i.id)
            patient_check = PatientByUser.objects.filter(user = request.user, patient__in = id_list).distinct(),id_list
            
            for i in obj_patient:
                for j in patient_check[1]:
                    if i.id == j:
                        patient.append(i)
                    else:
                        continue
            # patient = PatientDetails.objects.filter(id__in = patient_check[1])
         
        except:
            try:
                obj = PatientByUser.objects.get(user = request.user)
                patient = obj.patient.all().order_by('-id')
            except:
                self.context = {'status' : status.HTTP_400_BAD_REQUEST, "details" : "data not found"}

        page = request.query_params.get('page')
        paginator = Paginator(patient,1)

        try:
            patient = paginator.page(page)
        except PageNotAnInteger:
            patient = paginator.page(1)
        except EmptyPage:
            patient = paginator.page(paginator.num_pages)

        if page == None:
            page = 1

        page = int(page)

        page = int(page)
        serializer = PatientDetailsSerializer(patient, many=True)
        self.context = {'status' : status.HTTP_202_ACCEPTED, 'data' : serializer.data, 'page': page, 'pages': paginator.num_pages}
        # print("--- %s seconds ---" % (time.time() - start_time))
        return
    
    def single_data_thread(self, pk):
        obj = PatientDetails.objects.filter(id = pk)
        serializer = PatientDetailsSerializer(obj, many=True)
        self.context = {'status' : status.HTTP_202_ACCEPTED, 'data' : serializer.data}
        return

    def create_data_thread(self, request):
        data = request.data
        file = request.FILES
        try:
            obj = PatientDetails.objects.create(
                name = data['name'],
                age = data['age'],
                gender = data['gender'],
                whichProof = data['whichProof'],
                proofId = data['proofId'],
                mobileNo = data['mobileNo'],
                email = data['email'],
                city = data['city'],
                state = data['state'],
                country = data['country'],
                zipcode = data['zipcode'],
                problem = data['problem'],
                problemDescription = data['problemDescription'],
                # patientImage = file['patientImage'],
            )
            try:
                patien_data = PatientByUser.objects.get(user = request.user)
                patien_data.patient.add(obj)
                patien_data.save()
            except:
                patien_data = PatientByUser.objects.create(user = request.user)
                patien_data.patient.add(obj)
                patien_data.save()
            
            self.context = {'status' : status.HTTP_201_CREATED, 'details' : 'Patient record successfully added!'}
        except:
            self.context = {'status' : status.HTTP_204_NO_CONTENT, 'details' : 'Patient not added!'}
        return



    def update_data_thread(self, request, pk):
        data = request.data
        file = request.FILES
        try:
            PatientDetails.objects.filter(
                user = request.user,
                id = pk,
            ).update(
                name = data['name'],
                age = data['age'],
                gender = data['gender'],
                whichProof = data['whichProof'],
                proofId = data['proofId'],
                mobileNo = data['mobileNo'],
                email = data['email'],
                city = data['city'],
                state = data['state'],
                country = data['country'],
                zipcode = data['zipcode'],
                problem = data['problem'],
                problemDescription = data['problemDescription'],
                # patientImage = f"patient-images/{file['patientImage']}",
            )
            self.context = {'status' : status.HTTP_201_CREATED, 'details' : 'Patient record successfully Update!'}
        except:
            self.context = {'status' : status.HTTP_204_NO_CONTENT, 'details' : 'Patient not Update!'}
        return

    
    def delete_data_thread(self, pk):
        PatientDetails.objects.filter(id = pk).delete()
        self.context = {'status' : status.HTTP_200_OK, 'data' : 'Patient Successfully Deleted.'}
        return
    
# {
# "name" : "Ajay",
# "gender" : "male",
# "mobileNo" : 8878401574,
# "email" : "visheshsolanki12345@gmail.com",
# "city" : "INDORE",
# "state" : "MP",
# "whichProof" : "Adhar",
# "proofId" : "1245746",
# "country" : "INDIA",
# "zipcode" : 452015,
# "problem" : "eye",
# "problemDescription" : "not watch TV"
# }

class AllPatientViewSet(viewsets.ViewSet):
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        class_obj = AllPatientGetData()
        patient_list = Thread(target=class_obj.all_data_thread, args=(request,))
        patient_list.start()
        patient_list.join()
        return Response(class_obj.context)

    def retrieve(self, request, pk=None):
        class_obj = AllPatientGetData()
        patient_ret = Thread(target=class_obj.single_data_thread, args=(pk,))
        patient_ret.start()
        patient_ret.join()
        return Response(class_obj.context)

    def create(self, request, pk=None):
        class_obj = AllPatientGetData()
        patient_create = Thread(target=class_obj.create_data_thread, args=(request,))
        patient_create.start()
        patient_create.join()
        return Response(class_obj.context)

    def update(self, request, pk=None):
        class_obj = AllPatientGetData()
        patient_create = Thread(target=class_obj.update_data_thread, args=(request, pk))
        patient_create.start()
        patient_create.join()
        return Response(class_obj.context)

    def destroy(self, request, pk=None):
        class_obj = AllPatientGetData()
        patient_ret = Thread(target=class_obj.delete_data_thread, args=(pk,))
        patient_ret.start()
        patient_ret.join()
        return Response(class_obj.context)

    
