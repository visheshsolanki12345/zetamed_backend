from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from threading import Thread
from django.contrib.auth.models import User
from . import signals
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import (
    PatientDetails, PatientByUser, PatientGroup,
    PatientGroupByUser,
)
from .serializer import (
    PatientDetailsSerializer, PatientByUserSerializer, PatientGroupSerializer, PatientInfoSerializer
)
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
import time
import re

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

        UUID_PATTERN = re.compile(r'^[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$', re.IGNORECASE)
        if query_filter != '':
            if UUID_PATTERN.match(query_filter):
                patient = obj.patient.filter(
                    patientGroupId=query_filter
                ).values(
                        'id', 'name', 'age', 'gender', 'mobileNo', 
                        'email', 'problem', 'createAt', "patientImage"
                    ).order_by('-createAt')
            else:
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
                patient = obj.patient.all().values(
                    'id', 'name', 'age', 'gender', 'mobileNo', 
                    'email', 'problem', 'createAt', "patientImage"
                ).order_by('-createAt')
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
        group_id = ''
        for i in obj:
            group_id = str(i.patientGroupId)
        try:
            obj_group = PatientGroup.objects.get(id = group_id)
            serializer = PatientInfoSerializer(obj, many=True)
            self.context = {
                'status': status.HTTP_202_ACCEPTED, 
                'data': serializer.data,
                'patientGroup': obj_group.disease,
                'patientGroupId': obj_group.id,
            }
            return
        except:
            serializer = PatientInfoSerializer(obj, many=True)
            self.context = {
                'status': status.HTTP_202_ACCEPTED, 
                'data': serializer.data,
                'patientGroup': "not",
                'patientGroupId': "not",
            }
            return
            

    def create_data_thread(self, request):
        data = request.data
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
                # patientGroupId = data["patientGroup"],
            )
            group_obj = PatientGroup.objects.get(id = data["patientGroup"])
            obj.patientGroupId = group_obj
            obj.save()
            signals.patient_profile_data.send(sender=None, request=request, obj = obj)
            # context = {}
            # context_data = {}
            try:
                # patient_list = []
                # patint_group_id = data["patientGroup"]
                patien_data = PatientByUser.objects.get(user = request.user)
                # context_data = patien_data.patientGroup
                # if patint_group_id in context_data:
                #     for i in context_data[patint_group_id]:
                #         patient_list.append(i)
                #     patient_list.append(str(obj.id))
                #     context = context_data
                #     context[patint_group_id] = patient_list
                # else:
                #     context = context_data
                #     context[patint_group_id] = [str(obj.id)]
                patien_data.patient.add(obj)
                # patien_data.patientGroup = context
                patien_data.save()
            except:
                patien_data = PatientByUser.objects.create(user = request.user)
                # context[patint_group_id] = [str(obj.id)]
                # patien_data.patientGroup = context
                patien_data.patient.add(obj)
                patien_data.save()
            
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
                city = data['city'],
                state = data['state'],
                country = data['country'],
                zipcode = data['zipcode'],
                problem = data['problem'],
                problemDescription = data['problemDescription'],
                patientGroupId = data["patientGroup"],
            )

            obj = PatientDetails.objects.get(id = pk)
            group_obj = PatientGroup.objects.get(id = data["patientGroup"])
            obj.patientGroupId = group_obj
            obj.save()
            signals.patient_profile_data.send(sender=None, request=request, obj = obj)
            self.context = {'status' : status.HTTP_201_CREATED, 'details' : 'Patient record successfully Update!'}
        except:
            self.context = {'status' : status.HTTP_204_NO_CONTENT, 'details' : 'Patient not Update!'}
        return

    
    def delete_data_thread(self, pk):
        PatientDetails.objects.filter(id = pk).delete()
        self.context = {'status' : status.HTTP_200_OK, 'details' : 'Patient Successfully Deleted.'}
        return
    

class AllPatientGroupGetData:
    def __init__(self):
        self.context = ''
        Thread.__init__(self)

    def all_data_thread(self, request):
        obj_group = PatientGroupByUser.objects.get(user = request.user)
        # query_filter = request.query_params.get('query')
        # patient_group_data = ''
        # if query_filter == None:
        #     query_filter = ''
        # if query_filter != '':
        #     patient_group_data = obj_group.patientGroup.filter(disease = query_filter).order_by('-createAt')
        # else:
        #     patient_group_data = obj_group.patientGroup.all().order_by('-createAt')

        patient_group_data = obj_group.patientGroup.all().order_by('-createAt')
        # page = request.query_params.get('page')
        # paginator = Paginator(patient_group_data, 2)
        # try:
        #     patient_group_data = paginator.page(page)
        # except PageNotAnInteger:
        #     patient_group_data = paginator.page(1)
        # except EmptyPage:
        #     patient_group_data = paginator.page(paginator.num_pages)

        # if page == None:
        #     page = 1 
        # page = int(page)

        # page = int(page)
        serializer = PatientGroupSerializer(patient_group_data, many=True)
        self.context = {
            'status' : status.HTTP_202_ACCEPTED, 
            'data' : serializer.data,
            # 'page': page, 
            # 'pages': paginator.num_pages,
        }

    def single_data_thread(self, pk):
        obj = PatientGroup.objects.filter(id = pk)
        serializer = PatientGroupSerializer(obj, many=True)
        self.context = {'status' : status.HTTP_202_ACCEPTED, 'data' : serializer.data}
        return
    
    def create_data_thread(self, request):
        data = request.data
        obj = PatientGroup.objects.create(
            disease = data['disease'],
            diseaseDiscription = data['diseaseDiscription'],
        )
        try:
            patien_group_obj = PatientByUser.objects.get(user = request.user)
            patien_group_obj.patientGroup.add(obj)
            patien_group_obj.save()
        except:
            patien_group_obj = PatientGroupByUser.objects.create(user = request.user)
            patien_group_obj.patientGroup.add(obj)
            patien_group_obj.save()

    def update_data_thread(self, request, pk):
        data = request.data
        PatientGroup.objects.filter(
            id = pk,
        ).update(
            disease = data['disease'],
            diseaseDiscription = data['diseaseDiscription']
        )
        self.context = {'status' : status.HTTP_202_ACCEPTED, 'details' : 'Group Successfully Updated.'}
        return

    def delete_data_thread(self, pk):
        PatientGroup.objects.filter(id = pk).delete()
        self.context = {'status' : status.HTTP_200_OK, 'details' : 'Group Successfully Deleted.'}
        return

class AllPatientViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes=[JWTAuthentication]

    def list(self, request):
        class_obj = AllPatientGetData()
        patient_list = Thread(target=class_obj.all_data_thread, args=(request,))
        patient_list.start()
        patient_list.join()
        return Response(class_obj.context)

    def retrieve(self, request, pk=None):
        class_obj = AllPatientGetData()
        patient_ret = Thread(target=class_obj.single_data_thread, args=(request, pk))
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



class PatientGroupViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes=[JWTAuthentication]

    def list(self, request):
        class_obj = AllPatientGroupGetData()
        patient_gr_list = Thread(target=class_obj.all_data_thread, args=(request,))
        patient_gr_list.start()
        patient_gr_list.join()
        return Response(class_obj.context)

    def retrieve(self, request, pk=None):
        class_obj = AllPatientGroupGetData()
        patient_group_list = Thread(target=class_obj.single_data_thread, args=(pk,))
        patient_group_list.start()
        patient_group_list.join()
        return Response(class_obj.context)

    def create(self, request, pk=None):
        class_obj = AllPatientGroupGetData()
        patient_group_create = Thread(target=class_obj.create_data_thread, args=(request,))
        patient_group_create.start()
        patient_group_create.join()
        return Response(class_obj.context)

    def update(self, request, pk=None):
        class_obj = AllPatientGroupGetData()
        patient_group_update = Thread(target=class_obj.update_data_thread, args=(request, pk))
        patient_group_update.start()
        patient_group_update.join()
        return Response(class_obj.context)

    def destroy(self, request, pk=None):
        class_obj = AllPatientGroupGetData()
        patient_ret = Thread(target=class_obj.delete_data_thread, args=(pk,))
        patient_ret.start()
        patient_ret.join()
        return Response(class_obj.context)

    
