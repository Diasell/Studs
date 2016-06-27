from django.contrib.auth.models import User, Group
from rest_framework import serializers

from students.models import ProfileModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'groups',
            'first_name',
            'last_name'
        )


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            'name'
        )


class StudentSerializer(serializers.ModelSerializer):
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
