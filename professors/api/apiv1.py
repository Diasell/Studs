import datetime
# from datetime import timedelta
# from django.contrib.auth import authenticate

from rest_framework import status

from django.contrib.auth.models import User


from rest_framework.authentication import (
    TokenAuthentication,
    # BasicAuthentication,

)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


# from rest_framework import viewsets
# from rest_framework.authtoken.models import Token
# from students.api.serializers import (
#     UserSerializer,
#     GroupSerializer,
#     ProfileSerializer,
# )

from department.models import (
    Disciplines,
    ParaTime,
    Para,
    StartSemester
)
from professors.api.serializers import (
    StudentJournalSerializer
)
from students.models import (
    ProfileModel,
    StudentJournalModel
)


class StudentJournalInstanceView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    serializer_class = StudentJournalSerializer


    def post(self, request, *args, **kwargs):
        """
        Method to save StudentJournalModel instance for Professors users
        """
        user = request.user
        has_perm = user.has_perm('students.add_studentjournalmodel')
        if user.is_active:
            if has_perm:
                value = self.request.data['value']
                date = self.request.data['date']
                discipline = self.request.data['discipline']
                para_number = self.request.data['para_number']
                student = self.request.data['student']
                is_module = self.request.data['is_module']

                try:
                    new_instance = StudentJournalModel.objects.create(
                        value=value,
                        date=date,
                        discipline=Disciplines.objects.get(discipline=discipline),
                        para_number=ParaTime.objects.get(para_position=para_number),
                        student=User.objects.get(username=student),
                        is_module=is_module
                    )
                except Exception:
                    return Response({"Failed": "Not valid data"},
                                    status=status.HTTP_403_FORBIDDEN)
                new_instance.save()
                serialized = StudentJournalSerializer(new_instance)
                return Response(serialized.data, status=status.HTTP_201_CREATED)
            return Response({"Permissions": "User has not enough permissions"},
                            status=status.HTTP_403_FORBIDDEN)
        return Response({"Authorization": "This is not an active user"},
                        status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, *args, **kwargs):
        """
        Method that allows professor user to edit the StudentJournalModel instance
        """
        user = request.user
        has_perm = user.has_perm('students.change_studentjournalmodel')
        if user.is_active:
            if has_perm:
                pk = self.request.data['pk']
                value = self.request.data['value']
                date = self.request.data['date']
                discipline = self.request.data['discipline']
                para_number = self.request.data['para_number']
                student = self.request.data['student']
                is_module = self.request.data['is_module']

                edit_obj = StudentJournalModel.objects.get(pk=pk)
                try:
                    edit_obj.value = value
                    edit_obj.date = date
                    edit_obj.discipline = Disciplines.objects.get(discipline=discipline)
                    edit_obj.para_number = ParaTime.objects.get(para_position=para_number)
                    edit_obj.student = User.objects.get(username=student)
                    edit_obj.is_module = is_module
                except Exception:
                    return Response({"Failed": "Not valid data"},
                                    status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
                edit_obj.save()
                serialized = StudentJournalSerializer(edit_obj)
                return Response(serialized.data, status=status.HTTP_201_CREATED)
            return Response({"Permissions": "User has not enough permissions"},
                            status=status.HTTP_403_FORBIDDEN)
        return Response({"Authorization": "This is not an active user"},
                        status=status.HTTP_401_UNAUTHORIZED)


class GroupsListView(APIView):
    """
    API endpoint that allows professor user to get
    the list of all the group that he is currently
    teaching(current Semester)
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        if user.is_active:
            todaysdate = datetime.date.today()
            current_semester = StartSemester.objects.get(
                semesterstart__lt=todaysdate,
                semesterend__gt=todaysdate
            )
            groups = Para.objects.filter(
                semester=current_semester,
                para_professor=ProfileModel.objects.get(user=user)
            ).values_list('para_group__title', flat=True).distinct()
            result = dict()
            for number, group in enumerate(groups):
                result[number+1] = group
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response({"Authorization": "This is not an active user"},
                            status=status.HTTP_401_UNAUTHORIZED)
