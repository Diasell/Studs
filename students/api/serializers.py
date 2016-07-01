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


class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disciplines
        fields = (
            'discipline',
        )


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        fields = (
            'room',
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
    para_subject = DisciplineSerializer()
    para_room = RoomSerializer()
    para_professor = ProfileSerializer(read_only=True)
    para_number = ParaTimeSerializer()
    para_day = WorkingDaySerializer()
    # para_group = StudentGroupSerializer()

    class Meta:
        model = Para
        fields = (
            'para_subject',
            'para_room',
            'para_professor', # TODO: serialize.data fucks up here( FIX NEEDED)
            'para_number',
            'para_day',
            'para_group',
            'week_type'
        )
