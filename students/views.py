from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from students.serializers import (
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
