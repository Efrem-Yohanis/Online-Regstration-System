from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import re
from rest_framework import status
from app1.models import *
from rest_framework.exceptions import PermissionDenied
from .serializers import CustomUserSerializer
import datetime
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from .mydecoretprs import require_fields,validate_fields
import re

@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getalluser(request):
    try:
        all_data = CustomUser.objects.all()
        serializer = CustomUserSerializer(all_data, many=True)
        data = {
            'code': 1000,
            'message': 'success',
            'data': serializer.data
        }
        return Response(data)
    except PermissionDenied:
        error_data = {
            'code': 403,
            'message': 'Forbidden',
        }
        return Response(error_data, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def registration(request):
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    email = request.data.get('email')
    username = request.data.get('username')
    password1 = request.data.get('password1')
    password2 = request.data.get('password2')
    phone = request.data.get('phone')
    address = request.data.get('address')
    role = request.data.get('role')
    date_of_birth = request.data.get('date_of_birth')

    if not re.match("^[a-zA-Z]*$", first_name):
        respond_data = {
            'code': 601,
            'message': 'First name should only contain letters',
        }
        return Response(respond_data)

    elif not re.match("^[a-zA-Z]*$", last_name):
        respond_data = {
            'code': 602,
            'message': 'Last name should only contain letters',
        }
        return Response(respond_data)

    elif not re.match("^[a-zA-Z]*$", username):
        respond_data = {
            'code': 603,
            'message': 'Username should only contain letters',
        }
        return Response(respond_data)

    elif not re.match(r'^\+[0-9]{1,3}\s?[0-9]{9,15}$', phone):
        respond_data = {
            'code': 604,
            'message': 'Phone number should be in the format +1234567890',
        }
        return Response(respond_data)

    elif password1 != password2:
        respond_data = {
            'code': 606,
            'message': 'Passwords do not match.',
        }
        return Response(respond_data)

    elif User.objects.filter(username=username).exists():
        respond_data = {
            'code': 607,
            'message': 'Username already exists',
        }
        return Response(respond_data)

    elif User.objects.filter(email=email).exists():
        respond_data = {
            'code': 608,
            'message': 'Email already exists',
        }
        return Response(respond_data)

    else:
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # Create your CustomUser object here
        new_user = CustomUser.objects.create(
            user=user, email=email, first_name=first_name, date_of_birth=date_of_birth, role=role,
            address=address, phone=phone, username=username, last_name=last_name
        )

        if new_user:
            respond_data = {
                'code': 1000,
                'message': 'User successfully created. Please login using username and password.',
            }
            return Response(respond_data)
        


@api_view(['PUT'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
@require_fields(['first_name', 'last_name', 'username', 'email', 'phone', 'address', 'role', 'date_of_birth'])
@validate_fields({
    'first_name': lambda x: x.isalpha(),
    'last_name': lambda x: x.isalpha(),
    'username': lambda x: x.isalpha(),
    'phone': lambda x: re.match(r'^\+[0-9]{1,3}\s?[0-9]{9,15}$', x),
    'date_of_birth': lambda x: datetime.datetime.strptime(x, "%Y-%m-%d").date(),
})

def update(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)

        first_name = request.data['first_name']
        last_name = request.data['last_name']
        username = request.data['username']
        email = request.data['email']
        phone = request.data['phone']
        address = request.data['address']
        role = request.data['role']
        date_of_birth = request.data['date_of_birth']

        birth_date = datetime.datetime.strptime(date_of_birth, "%Y-%m-%d").date()
        today = datetime.date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

        if age < 20:
            return Response({
                'code': 608,
                'message': 'Age must be above 20 years.',
            }, status=400)

        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.phone = phone
        user.address = address
        user.role = role
        user.date_of_birth = date_of_birth
        user.save()

        return Response({
            'code': 1000,
            'message': 'User information updated successfully.',
        })

    except CustomUser.DoesNotExist:
        return Response({
            'code': 404,
            'message': 'User not found.',
        }, status=404)
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_user(request, user_id):
    try:
        #user = User.objects.get(id=user_id)
        custom= CustomUser.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {'code': 404, 'message': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = CustomUserSerializer(custom)
    return Response(
        {'code': 1000, 'message': 'success', 'data': serializer.data},
        status=status.HTTP_200_OK
    )


@api_view(['PATCH'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def patch_req(request, user_id):
    try:
        user = CustomUser.objects.get(pk=user_id)
    except CustomUser.DoesNotExist:
        return Response({'code': 404, 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CustomUserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        response_data = {
            'code': 1000,
            'message': 'Successfully updated user',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    return Response({
        'code': 400,
        'message': 'Bad request',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)







@api_view(['DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def delete(request, user_id):
    try:
        user = request.user
        req_user = CustomUser.objects.get(user=user)
        
        if req_user.role == 'User':
            return Response({'detail': 'Sorry, this action is not allowed for you! It can only be done by the administrator.'}, status=status.HTTP_403_FORBIDDEN)

        user_to_delete = CustomUser.objects.get(id=user_id)
        if user.id == user_to_delete.user.id:
            return Response({'detail': 'You cannot delete your own account.'}, status=status.HTTP_400_BAD_REQUEST)

        user_to_delete.delete()
        return Response({'detail': 'User deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    except CustomUser.DoesNotExist:
        return Response({'code': 404, 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    

from django.http import HttpResponse
from django.views.decorators.http import require_http_methods


@api_view(['PATCH', 'OPTIONS'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def options_req(request, user_id):
    if request.method == 'OPTIONS':
        allowed_methods = ['PATCH', 'OPTIONS']
        response = Response()
        response['Allow'] = ', '.join(allowed_methods)
        response['Content-Length'] = '0'
        return response

    # Existing PATCH request handling code
    try:
        user = CustomUser.objects.get(pk=user_id)
    except CustomUser.DoesNotExist:
        return Response({'code': 404, 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CustomUserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        response_data = {
            'code': 1000,
            'message': 'Successfully updated user',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    return Response({
        'code': 400,
        'message': 'Bad request',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)