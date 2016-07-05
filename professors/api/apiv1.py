import datetime
from datetime import timedelta
from django.contrib.auth import authenticate

from rest_framework import status, views

from django.contrib.auth.models import User, Group


from rest_framework.authentication import (
    TokenAuthentication,
    BasicAuthentication,

)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from students.api.serializers import (
    UserSerializer,
    GroupSerializer,
    ProfileSerializer,
)
from professors.api.serializers import (
    StudentJournalSerializer
)
from students.models import (
    ProfileModel,
    StudentJournalModel
)


class JournalViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows professors edit students Journal
    """
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = StudentJournalModel.objects.all()
    serializer_class = StudentJournalSerializer