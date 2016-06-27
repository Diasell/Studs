import json

from django.contrib.auth import authenticate, login

from rest_framework import status, views
from rest_framework.response import Response

from django.contrib.auth.models import User, Group


from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticatedOrReadOnly
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
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request, format=None):

        print ".user" ,request.user
        username = request.user
        print ".auth",  request.auth

        data = request.DATA
        print ".data" ,data

        account = authenticate(username=username, password="1qaz0okm")

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


class ExampleView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(content)

    def post(self, request, format=None):
        username = request.data["username"]
        password = request.data["password"]

        account = authenticate(username=username, password=password)
        print type(account)

        if account is not None:
            if account.is_active:
                token = Token.objects.get_or_create(user=account)[0]
                print token
                return Response(
                    {'Authorization': "Token %s" % token},
                    status=status.HTTP_200_OK
                )
        else:
            return Response(
                {
                'status': 'Unauthorized',
                'message': 'Username/password combination is invalid'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )



