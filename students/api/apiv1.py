import datetime
from datetime import timedelta
from django.contrib.auth import authenticate

from rest_framework import status, views
from rest_framework.response import Response

from django.contrib.auth.models import User, Group


from rest_framework.authentication import (
    TokenAuthentication,
    BasicAuthentication,

)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from students.api.serializers import (
    UserSerializer,
    GroupSerializer,
    ProfileSerializer,
    ParaSerializer
)

from students.models import ProfileModel
from department.models import (
    Para,
    WorkingDay,
    StartSemester
)


def ifweekiseven(todaysdata, datastart):
    """
    Helper function that tracks what week is now from the certain
    day. For us it important when we calculate schedule as we  have to
    know whether it is even week or odd
    :param todaysdata: type datetime
    :param datastart: data when semester starts
    """

    weekday1e = datastart.weekday()
    mondaydelta = timedelta(weekday1e)
    monday = datastart - mondaydelta
    delta = ((todaysdata - monday) / 7).days + 1

    if delta % 2 == 0:
        return True
    else:
        return False


def get_weektype(date):
    """
    Checks what is the weektype
    :param date: datetime.date type value
    :return: True/False/None
    """
    semesters = StartSemester.objects.all()
    approxsemesterlength = 6 * 31
    for semester in semesters:
        difference = (date - semester.semesterstart).days
        if semester.semesterstart <= date and difference < approxsemesterlength:
            startsemesterdate = semester.semesterstart
            return ifweekiseven(date, startsemesterdate)
    return None


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows user groups to be viewed or edited.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows students to be viewed or edited
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = ProfileModel.objects.filter(is_student=True)
    serializer_class = ProfileSerializer


class LoginAPIView(APIView):
    """
    API that allows users to get a Token while authorization
    """
    authentication_classes = (BasicAuthentication,)
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        username = request.data["username"]
        password = request.data["password"]

        account = authenticate(username=username, password=password)

        if account is not None:
            if account.is_active:
                token = Token.objects.get_or_create(user=account)[0]
                return Response(
                    {'Authorization': "Token %s" % token},
                    status=status.HTTP_200_OK
                )
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Username/password combination is invalid'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )


class StudentTodayScheduleView(views.APIView):
    """
    API that returns JSON with schedule for user who is requesting
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        user = request.user
        print user
        usergroup = ProfileModel.objects.filter(user=user)[0].student_group
        current_weekday = datetime.date.today().weekday()  # integer 0-monday .. 6-Sunday
        today = WorkingDay.objects.get(dayoftheweeknumber=current_weekday)

        todaysdate = datetime.date.today()
        weektype = get_weektype(todaysdate)

        classes_for_today = Para.objects.filter(
            para_group=usergroup,
            para_day=today,
            week_type=weektype
        )
        print len(classes_for_today), classes_for_today
        result = dict()
        for i, para in enumerate(classes_for_today):
            result["para_%s"%i] = ParaSerializer(para).data
        return Response(result, status=status.HTTP_200_OK)

