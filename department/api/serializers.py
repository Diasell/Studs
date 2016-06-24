from django.contrib.auth.models import User, Group
from rest_framework import serializers

from department.models import (
    DepartmentModel,
    FacultyModel,
    StudentGroupModel
)


class FacultySerializer(serializers.ModelSerializer):

    class Meta:
        model = FacultyModel
        fields = (
            'title',
            'dean',
            'department_address',
        )


class DepartmentSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer()

    class Meta:
        model = DepartmentModel
        fields = (
            'faculty',
            'title',
            'leader'
        )


class StudentGroupSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()

    class Meta:
        model = StudentGroupModel
        fields = (
            'department',
            'title',
            'leader',
            'mentor',
            'date_started'
        )
