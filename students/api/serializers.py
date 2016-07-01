from django.contrib.auth.models import User, Group
from rest_framework import serializers

from students.models import ProfileModel
from department.models import (
    FacultyModel,
    DepartmentModel,
    StudentGroupModel,
    Disciplines,
    Para,
    ParaTime,
    Rooms,
    WorkingDay
)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            'name',
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name'
        )


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ProfileModel
        fields = (
            'user',
            'is_student',
            'is_professor',
            'student_group',
            'middle_name',
            'contact_phone',
            'photo',
            'started_date'
        )


class StudentGroupSerializer(serializers.ModelSerializer):
    leader = UserSerializer(read_only=True)
    mentor = UserSerializer(read_only=True)

    class Meta:
        model = StudentGroupModel

        fields = (
            '',
        )


class FacultySerializer(serializers.ModelSerializer):
    dean = UserSerializer(read_only=True)

    class Meta:
        model = FacultyModel
        fields = (
            'title',
            'dean',
            'department_address'
        )


class DepartmentSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer()
    leader = UserSerializer(read_only=True)

    class Meta:
        model = DepartmentModel
        fields = (
            'faculty',
            'title',
            'leader'
        )


class ParaTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParaTime
        fields = (
            'para_starttime',
            'para_endtime',
            'para_position'
        )


class WorkingDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingDay
        fields = (
            'dayoftheweek',
        )


class ParaSerializer(serializers.ModelSerializer):
    discipline = serializers.CharField(
        source='para_subject.discipline',
        read_only=True)
    room = serializers.CharField(
        source='para_room.room',
        read_only=True
    )
    professors_lastname = serializers.CharField(
        source='para_professor.user.last_name',
        read_only=True
    )
    professors_firstname = serializers.CharField(
        source='para_professor.user.first_name',
        read_only=True,
    )
    professors_middlename = serializers.CharField(
        source='para_professor.middle_name',
        read_only=True,
    )
    para_number = serializers.CharField(
        source='para_number.para_position',
        read_only=True,
    )
    para_day = serializers.CharField(
        source='para_day.dayoftheweek',
        read_only=True
    )
    para_group = serializers.CharField(
        source='para_group.title'
    )

    class Meta:
        model = Para
        fields = (
            'discipline',
            'room',
            'professors_lastname',
            'professors_firstname',
            'professors_middlename',
            'para_number',
            'para_day',
            'para_group',
            'week_type'
        )
