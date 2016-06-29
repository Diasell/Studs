from django.contrib.auth import authenticate

from rest_framework import status, views
from rest_framework.response import Response

from django.contrib.auth.models import User, Group


from rest_framework.authentication import (
    TokenAuthentication,
    BasicAuthentication,
    SessionAuthentication
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from students.api.serializers import (
    UserSerializer,
    GroupSerializer,
    StudentSerializer)

from students.models import ProfileModel


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    authentication_classes = (TokenAuthentication,)
    queryset = User.objects.all()
    serializer_class = UserSerializer



class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows user groups to be viewed or edited.
    """
    authentication_classes = (TokenAuthentication,)
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows students to be viewed or edited
    Returns Token
    """
    authentication_classes = (TokenAuthentication,)
    queryset = ProfileModel.objects.filter(is_student=True)
    serializer_class = StudentSerializer


class LoginAPIView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        username = request.data["username"]
        password = request.data["password"]

        account = authenticate(username=username, password=password)

        if account is not None:
            if account.is_active:
                token = Token.objects.get_or_create(user=account)[0]
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


class StudentScheduleView(views.APIView):
    """
    API that returns JSON with schedule for user who is requesting
    """
    authentication_classes = (TokenAuthentication,)

    def get(self, request, format=None):
        username = request.user

        # TODO: Create api view that would return logged in user schedule

