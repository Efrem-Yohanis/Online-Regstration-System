from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from app1.models import *
from django.http import JsonResponse
from .serializers import *
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

   
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getalluser(request):
    users = request.user
    print(users)
    # if not request.user.is_authenticated:
    #     return Response({"code": 403, "message": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

    # users = CustomUser.objects.all()
    serializer = CustomUserSerializer(users, many=True)
    res_data = {
        "code": 1000,
        "message": "Success",
        "data": serializer.data
    }
    return Response(res_data, status=status.HTTP_200_OK)



# post request fro registration
# get request to get all data
# get request to get single data
# delete singel data olny for admin 
# delete alwed olny for admin delete request single
# put request for update 



class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
 