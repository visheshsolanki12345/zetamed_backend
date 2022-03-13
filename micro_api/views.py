from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Country, State, City
from .serializer import CountrySerializer, StateSerializer, CitySerializer
# Create your views here.


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def country_state_city(request):
    obj = Country.objects.all()
    serializer = CountrySerializer(obj, many=True)
    context = {"status" : 200, "data" : serializer.data}
    return Response(context)