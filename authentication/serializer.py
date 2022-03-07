
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from authentication.models import Profile

class UserSerializer(serializers.ModelSerializer):
    isAdmin = serializers.SerializerMethodField(read_only=True)
    access = serializers.SerializerMethodField(read_only=True)
    token = serializers.SerializerMethodField(read_only=True)

    def get__id(self, obj):
        return obj.id

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_access(self, obj):
        return str(AccessToken.for_user(obj))
    
    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

class UserSerializerWithToken(UserSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name','last_name', 'isAdmin', 'token', 'access']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
        'id', 'user', 'mobileNo', 'iAm', 'speciality', 'clinicName', 
        'profileImage', 'createdAt',
        ]

    
class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)