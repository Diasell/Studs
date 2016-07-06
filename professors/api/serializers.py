from django.contrib.auth.models import User, Group
from rest_framework import serializers
from department.models import (
    Disciplines,
    ParaTime
)
from students.models import (
    StudentJournalModel
)


class StudentJournalSerializer(serializers.ModelSerializer):
    student = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )
    discipline = serializers.SlugRelatedField(
        queryset=Disciplines.objects.all(),
        slug_field='discipline'
    )
    para_number = serializers.SlugRelatedField(
        queryset=ParaTime.objects.all(),
        slug_field='para_position'
    )

    class Meta:
        model = StudentJournalModel
        fields = (
            'pk',
            'value',
            'date',
            'discipline',
            'para_number',
            'student',
            'is_module'
        )
