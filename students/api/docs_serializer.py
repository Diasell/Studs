from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from students.models import (
    ProfileModel,
    StudentJournalModel
)
from department.models import (
    FacultyModel,
    DepartmentModel,
    StudentGroupModel,
    Para,
    ParaTime,
    WorkingDay
)

class RegisterViewSerializer(serializers.ModelSerializer):
    """
    Serializer for DRF DOCS for REGISTRATION EndPoint
    """
    username = serializers.CharField(
        source='user.username',
    )
    password = serializers.CharField(
        source='user.password',
    )
    confirm_password = serializers.CharField(
        source='user.password'
    )
    email = serializers.EmailField(
        source='user.email',
    )
    last_name = serializers.CharField(
        source='user.last_name',
    )
    first_name = serializers.CharField(
        source='user.first_name',
    )
    faculty = serializers.CharField(
        source='faculty.title',
    )
    group_title = serializers.CharField(
        source='student_group.title'
    )
    group_started = serializers.CharField(
        source='student_group.started_date'
    )

    class Meta:
        model = ProfileModel
        fields = (
            'username',
            'email',
            'last_name',
            'first_name',
            'password',
            'confirm_password',
            'faculty',
            'group_title',
            'group_started',
            'birthday',
            'photo',
        )

class LoginViewSerializer(serializers.ModelSerializer):
    """
        Serializer for DRF DOCS for Login EndPoint
        """
    class Meta:
        model = User
        fields = (
            'username',
            'password'
        )
class AuthorizationSerializer(serializers.ModelSerializer):
    """
    Serializer for DRF DOCS for Login EndPoint
    """
    Authorization = serializers.CharField(
        source='key'
    )
    class Meta:
        model = Token
        fields = (
            'Authorization',
        )


class GroupStudentsSerializer(serializers.ModelSerializer):
    """
    Serializer for DRF DOCS to show all the students
    for the given group
    """
    group = serializers.CharField(
        source='user_student_group.title'
    )
    class Meta:
        model = Token
        fields = (
            'group',
        )

class GetStJournalSerializer(serializers.ModelSerializer):
    """
    Serializer for DRF DOCS to get students results for given
    student, discipline, range(default range is whole current semester)
    """
    start_date = serializers.DateField(
        source='date'
    )
    end_date = serializers.DateField(
        source='date'
    )
    student = serializers.CharField(
        source='student_username'
    )
    discipline = serializers.CharField(
        source='discipline_title'
    )
    class Meta:
        model = StudentJournalModel
        fields = (
            'start_date',
            'end_date',
            'student',
            'discipline'
        )