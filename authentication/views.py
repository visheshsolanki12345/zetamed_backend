from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from . import comman_function
from rest_framework import status
from threading import Thread
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from rest_framework_simplejwt.backends import TokenBackend
from . import signals
from .models import OtpVerify, Profile
from .serializer import (
    ProfileSerializer, UserSerializerWithToken, ChangePasswordSerializer
    )

# Create your views here.


class SendOTPThread:
    def __init__(self):
        Thread.__init__(self,)
        self.context = ''
    
    def send_otp_thread(self, request):
        set_signal = ''
        set_count_signal = ''
        data = request.data
        if type(data['mobileNo']) == int:
            checkNo = OtpVerify.objects.filter(mobileNo = data['mobileNo'], isVerify = True).exists()
            if checkNo:
                self.context = {'status' : status.HTTP_208_ALREADY_REPORTED, 'details' : 'You allready Message Verify please you should go register or login'}
                set_signal = False

            obj_time_count = OtpVerify.objects.filter(mobileNo = data['mobileNo'], maxTry = 3)
            if obj_time_count:
                time_threshold = datetime.now() - timedelta(minutes=24)
                obj_time_count = OtpVerify.objects.filter(mobileNo = data['mobileNo'], maxTry = 3, createAt__lt = time_threshold)
                if obj_time_count:
                    set_signal = True
                    set_count_signal = True
                else:
                    self.context = {'status' : status.HTTP_304_NOT_MODIFIED, 'details' : 'You not resent otp until 24 hourse'} 
                    set_signal = False
            else:
                set_signal = True
        else:
             self.context = {
                 'status' : status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, 
                 'details' : 'You not fill right data'
                }

        if set_signal == True:
            otp = comman_function.otp_generate()
            msg = f"Hello There this is your OTP {otp}"
            msg_status, msg_id = comman_function.otp_request_twillo(data['mobileNo'], msg)
            check_update = OtpVerify.objects.filter(mobileNo = data['mobileNo']).exists()
            if check_update:
                obj_count = OtpVerify.objects.get(
                    mobileNo = data['mobileNo']
                )
                if set_count_signal:
                    obj_count.maxTry = 1
                obj_count.maxTry += 1
                obj_count.msgStatus = msg_status
                obj_count.isOtp = otp
                obj_count.save()
            else:
                OtpVerify.objects.create(
                    mobileNo = data['mobileNo'],
                    isOtp = otp,
                    msgStatus = msg_status,
                    msgId = msg_id,
                )
            context = {
                'status' : status.HTTP_202_ACCEPTED, 
                'mobileNo' : data['mobileNo']
                }
            set_signal = True
            self.context = context
            return
        return 

class MsgOtpVerify:
    def __init__(self):
        Thread.__init__(self,)
        self.context = ''
    
    def otp_verify_thread(self, request):
        data = request.data
        obj_find = OtpVerify.objects.filter(mobileNo = data['mobileNo'])
        if obj_find:
            time_threshold = datetime.now() - timedelta(minutes=10)
            obj_time_count = OtpVerify.objects.filter(mobileNo = data['mobileNo'], createAt__gt = time_threshold)
            if obj_time_count:
                for i in obj_time_count:
                    if data['isOtp'] == i.isOtp:
                        obj_time_count.update(isVerify = True)
                        self.context = {'status' : status.HTTP_200_OK, 'details' : 'Your Otp is verify'}
                        return
                    else:
                        self.context = {'status' : status.HTTP_204_NO_CONTENT, 'details' : 'Your Otp is not verify'}
                        return
            else:
                self.context = {'status' : status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, 'details' : 'Your Otp is expiry'}
                return
        else:
            self.context = {'status' : status.HTTP_400_BAD_REQUEST, 'details' : 'Not Verify your mobile No.'}
            return


class RegisterUserAuth:
    def __init__(self):
        Thread.__init__(self)
        self.context = ''

    def register_user_thread(self, request):
        data = request.data
        email_check = comman_function.email_check_validation(data['email'])
        if email_check == False:
            self.context = {'status' : status.HTTP_400_BAD_REQUEST, 'details' : 'Please fill proper email'}
            return
        elif len(str(data['password'])) <= 8:
            self.context = {'status' : status.HTTP_400_BAD_REQUEST, 'details' : 'Password should be 8 digit also with @ A-Z, 1 to 100'}
            return
        elif User.objects.filter(email = data['email']).exists() == True:
            self.context = {'status' : status.HTTP_208_ALREADY_REPORTED, 'details' : 'This email allready exists'}
            return
        else:
            try:    
                user = User.objects.create(
                    first_name= data['first_name'],
                    last_name=data['last_name'],
                    username=data['email'],
                    email=data['email'],
                    password=make_password(data['password'])
                )
                self.context = UserSerializerWithToken(user, many=False).data
                signals.user_profile_data.send(sender=None, request=request, user=self.context['id'])
                return
            except:
                self.context = {'status' : status.HTTP_208_ALREADY_REPORTED, 'details' : 'Please make strong password'}
            return

class UserDataUpdate:
    def __init__(self):
        Thread.__init__(self)
        self.context = ''

    def user_data_update_thread(self, request, pk):
        data = request.data
        file = request.FILES
        email_check = comman_function.email_check_validation(data['email'])
        if email_check == False:
            self.context = {'status' : status.HTTP_400_BAD_REQUEST, 'details' : 'Please fill proper email'}
            return
        elif User.objects.filter(email = data['email']).exists() == True:
            self.context = {'status' : status.HTTP_400_BAD_REQUEST, 'details' : 'This email allready exists'}
            return
        else:
            User.objects.filter(id = pk).update(
                first_name= data['first_name'],
                last_name=data['last_name'],
                username=data['email'],
                email=data['email'],
                # profileImage = f"profile-images/{file['profileImage']}",
            )
            self.context = {'status' : status.HTTP_202_ACCEPTED, "details" : "User details successfully changed"}
            return       


class UserProfileDataUpdate:
    def __init__(self):
        Thread.__init__(self)
        self.context = ''

    def user_profile_update_thread(self, request, pk):
        data = request.data
        file = request.FILES
        Profile.objects.filter(id = pk).update(
            iAm=data['iAm'],
            speciality=data['speciality'],
            clinicName=data['clinicName'],
            profileImage = f"profile-images/{file['profileImage']}",
        )
        self.context = {'status' : status.HTTP_201_CREATED, "details" : "User Profile successfully changed"}
        return     

class GetUserFromToken:
    def __init__(self):
        Thread.__init__(self)
        self.context = ''
    def find_user_from_token_thread(self, token):
        try:
            valid_data = TokenBackend(algorithm='HS256').decode(token,verify=False)
            userId = valid_data['user_id']
            user_data = User.objects.filter(id=userId)
            serializer = UserSerializerWithToken(user_data, many=True)
            self.context = {'status' : status.HTTP_200_OK, 'data' : serializer.data}
            return 
        except:
            self.context = {'error':'This is not valid user', 'status':status.HTTP_401_UNAUTHORIZED}
            return 

class GetUserProfile:
    def __init__(self, request):
        self.request = request
        Thread.__init__(self)
        self.user = self.request.user
        obj = Profile.objects.filter(user = self.user)
        serializer = ProfileSerializer(obj, many=True)
        self.context = serializer.data
        return
    
                 
# {
# "first_name" : "vishesh",
# "last_name" : "solanki",
# "email" : "visheshsolanki1234@gmail.com",
# "password" : "vishesh@123",
# "mobileNo" : 8878401574,
# "iAm" : "Doctore",
# "speciality" : "eye",
# "clinicName" : "Zetamonk"
# }

# {
# "first_name" : "vishesh",
# "last_name" : "solanki",
# "email" : "visheshsolanki234@gmail.com"
# }

##========================== Send Otp =====================================##
@api_view(['POST'])
def send_otp(request):
    class_obj = SendOTPThread()
    sentotp = Thread(target=class_obj.send_otp_thread, args=(request, ))
    sentotp.start()
    sentotp.join()
    
    context_data = class_obj.context
    status = class_obj.context['status']
    if status == 202:
        return Response(context_data)
    return Response(context_data)


##========================== Otp Verify =====================================##
@api_view(['POST'])
def otp_verify(request):
    class_obj = MsgOtpVerify()
    verifyotp = Thread(target=class_obj.otp_verify_thread, args=(request,))
    verifyotp.start()
    verifyotp.join()
    context_data = class_obj.context
    return Response(context_data)


##========================== User Register =====================================##
@api_view(['POST'])
def user_register(request):
    class_obj = RegisterUserAuth()
    user_reg = Thread(target=class_obj.register_user_thread, args=(request,))
    user_reg.start()
    user_reg.join()
    context_data = class_obj.context
    return Response(context_data)


##==========================  Login =====================================##
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


##========================== Password change =====================================##
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


##========================== User info Change =====================================##
@api_view(['POST'])
# @authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_data_change(request, pk):
    class_obj = UserDataUpdate()
    user_change = Thread(target=class_obj.user_data_update_thread, args=(request, pk))
    user_change.start()
    user_change.join()
    context_data = class_obj.context
    return Response(context_data)

##========================== User info Change =====================================##
@api_view(['POST'])
# @authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_profile_change(request, pk):
    class_obj = UserProfileDataUpdate()
    user_profile = Thread(target=class_obj.user_profile_update_thread, args=(request, pk))
    user_profile.start()
    user_profile.join()
    context_data = class_obj.context
    return Response(context_data)

##========================== User find from token =====================================##
@api_view(['GET'])
# @authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def find_user_by_token(request, token):
    class_obj = GetUserFromToken()
    user_data = Thread(target=class_obj.find_user_from_token_thread, args=(token,))
    user_data.start()
    user_data.join()
    context_data = class_obj.context
    return Response(context_data)

##========================== User find from token =====================================##
@api_view(['GET'])
# @authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    class_obj = GetUserProfile(request)
    context_data = class_obj.context
    return Response(context_data)
