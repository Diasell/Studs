from django.contrib.auth.models import User, Group
from rest_framework import serializers

from students.models import (
    StudentJournalModel
)


class StudentJournalSerializer(serializers.ModelSerializer):

    discipline = serializers.CharField(
        source='discipline.discipline'
    )
    student = serializers.CharField(
        source='student.username',
        read_only=True,
    )

    class Meta:
        model = StudentJournalModel
        fields = (
            'value',
            'date',
            'discipline',
            'student',
            'is_module'
        )