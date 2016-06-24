from django.contrib.auth.models import User, Group
from rest_framework import serializers

from students.models import ProfileModel


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'url',
            'username',
            'email',
            'groups',
            'first_name',
            'last_name'
        )


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = (
            'url',
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
