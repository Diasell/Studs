import json

from django.contrib.auth import authenticate, login

from rest_framework import status, views
from rest_framework.response import Response

from django.contrib.auth.models import User, Group

from rest_framework import viewsets
from students.api.serializers import (
    UserSerializer,
    GroupSerializer,
    StudentSerializer)

from students.models import ProfileModel


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows user groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows students to be viewed or edited
    """
    queryset = ProfileModel.objects.filter(is_student=True)
    serializer_class = StudentSerializer


class LoginAPIview(views.APIView):
    """
    API endpoint for users to login though API
    """

    def post(self, request, format=None):

        print ".user" ,request.user
        username = request.user
        print ".auth",  request.auth

        password = request.
        print ".pass" ,password

        account = authenticate(username=username, password=password)

        if account is not None:
            if account.is_active:
                login(request, account)

                serialized = UserSerializer(account)

                return Response(serialized.data)
            else:
                return Response({
                    'status': 'Unauthorized',
                    'message': 'This account has been disabled.'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Username/password combination invalid.'
            }, status=status.HTTP_401_UNAUTHORIZED)



