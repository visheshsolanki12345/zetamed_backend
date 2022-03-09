from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from threading import Thread
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import PatientDetails
from .serializer import PatientDetailsSerializer

# Create your views here.
class AllPatientGetData:
    def __init__(self):
        self.context = ''
        Thread.__init__(self)

    def all_data_thread(self, request):
        obj = PatientDetails.objects.filter(user = request.user)
        serializer = PatientDetailsSerializer(obj, many=True)
        print(serializer.data)
        self.context = {'status' : status.HTTP_202_ACCEPTED, 'data' : serializer.data}
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
            PatientDetails.objects.create(
                user = request.user,
                name = data['name'],
                age = data['age'],
                gender = data['gender'],
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
    

class AllPatientViewSet(viewsets.ViewSet):
    # authentication_classes=[JWTAuthentication]
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

    
