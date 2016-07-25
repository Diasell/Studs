import datetime
from datetime import timedelta
from django.contrib.auth import authenticate

from rest_framework import status, views
from rest_framework.parsers import (
    MultiPartParser,
    JSONParser
)
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
from professors.api.serializers import (
    StudentJournalSerializer
)

from students.models import (
    ProfileModel,
    StudentJournalModel
)
from department.models import (
    Para,
    WorkingDay,
    StartSemester,
    Disciplines,
    StudentGroupModel,
    FacultyModel
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
    authentication_classes = (BasicAuthentication,)
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
                user = User.objects.get(username=username)
                profile = ProfileModel.objects.get(user=user)

                response = dict()
                response['Authorization'] = "Token %s" % token
                response['full_name'] = user.get_full_name()
                response['email'] = user.email
                photo = ProfileSerializer(profile).data['photo']
                response['photo'] = photo
                response['group'] = profile.student_group.title
                response['faculty'] = profile.faculty.title

                return Response(
                    response,
                    status=status.HTTP_200_OK
                )
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Username/password combination is invalid'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )


class RegisterAPIView(APIView):
    """
    API that allows users to register a new account
    """
    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser, JSONParser)

    def post(self, request, format=None):
        # getting data from user request
        username = request.data["username"]
        password = request.data["password"]
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        c_password = request.data['confirm_password']
        group = request.data['group']
        faculty = request.data['faculty']
        email = request.data['email']
        photo = request.FILES['file']

        errors = dict()
        # validating the uploaded file
        if photo:
            if photo.size > (2048 * 1024):
                errors['photo'] = u"Size of the image shouldn't be greater than 2Mb"
            elif not ('image' in photo.content_type):
                errors['photo'] = u"File type should be an image"

        # basic validation for user details
        if User.objects.filter(username=username):
            errors['username'] = u"username is already taken"
        if User.objects.filter(email=email):
            errors['email'] = u"email is already taken"
        if password != c_password:
            errors['password'] = u"passwords doesn't match"

        if errors:
            return Response(errors,status=status.HTTP_403_FORBIDDEN)

        serialized = UserSerializer(data=request.data).is_valid()
        if serialized:
                new_user = User.objects.create_user(
                    username=username,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    email=email
                )
                user_group = StudentGroupModel.objects.get(title=group)
                new_user_profile = ProfileModel.objects.create(
                    user=new_user,
                    is_student=True,
                    student_group=user_group,
                    faculty=FacultyModel.objects.get(title=faculty),
                    started_date=user_group.date_started,
                    photo=photo
                )

                token = Token.objects.get_or_create(user=new_user)[0]
                print token
                user = new_user
                profile = new_user_profile

                response = dict()
                response['Authorization'] = "Token %s" % token
                response['full_name'] = user.get_full_name()
                response['email'] = user.email
                response['group'] = profile.student_group.title
                response['faculty'] = profile.faculty.title

                return Response(
                    response,
                    status=status.HTTP_201_CREATED
                )
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Provided data is invalid'
                },
                status=status.HTTP_403_FORBIDDEN
            )


class TodayScheduleView(views.APIView):
    """
    API that returns JSON with schedule for user who is requesting
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        user = request.user
        todaysdate = datetime.date.today()
        weektype = get_weektype(todaysdate)
        current_weekday = datetime.date.today().weekday()  # integer 0-monday .. 6-Sunday
        today = WorkingDay.objects.get(dayoftheweeknumber=current_weekday)
        if user.is_active:
            if ProfileModel.objects.get(user=user).is_student:
                student_group = ProfileModel.objects.get(user=user).student_group

                classes_for_today = Para.objects.filter(
                    para_group=student_group,
                    para_day=today,
                    week_type=weektype
                )
                result = dict()
                for i, para in enumerate(classes_for_today):
                    result["para_%s" % i] = ParaSerializer(para).data
                return Response(result, status=status.HTTP_200_OK)
            elif ProfileModel.objects.get(user=user).is_professor:
                classes_for_today = Para.objects.filter(
                    para_professor=ProfileModel.objects.get(user=user),
                    para_day=today,
                    week_type=weektype
                )
                result = dict()
                for i, para in enumerate(classes_for_today):
                    result["para_%s" % i] = ParaSerializer(para).data
                return Response(result, status=status.HTTP_200_OK)
        else:
            return Response({"UnAuth": "Current user is not active"},
                            status=status.HTTP_401_UNAUTHORIZED)


class WeeklyScheduleView(views.APIView):
    """
    API endpoint to get user schedule for current week
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        user = request.user
        todaysdate = datetime.date.today()
        weektype = get_weektype(todaysdate)
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        result = dict()
        if user.is_active:
            if ProfileModel.objects.get(user=user).is_student:
                student_group = ProfileModel.objects.get(user=user).student_group
                for day in range(0, 5):
                    classes = Para.objects.filter(
                        para_group=student_group,
                        para_day__dayoftheweeknumber=day,
                        week_type=weektype
                    )
                    day_js = dict()
                    for i, para in enumerate(classes):
                        day_js["para_%s" % i] = ParaSerializer(para).data

                    result["%s" % days[day]] = day_js
                return Response(result, status=status.HTTP_200_OK)
            elif ProfileModel.objects.get(user=user).is_professor:
                for day in range(0, 5):
                    classes = Para.objects.filter(
                        para_professor=ProfileModel.objects.get(user=user),
                        para_day__dayoftheweeknumber=day,
                        week_type=weektype
                    )
                    day_js = dict()
                    for i, para in enumerate(classes):
                        day_js["para_%s" % i] = ParaSerializer(para).data

                    result["%s" % days[day]] = day_js
                return Response(result, status=status.HTTP_200_OK)
        else:
            return Response({"UnAuth": "Current user is not active"},
                            status=status.HTTP_401_UNAUTHORIZED)


class GroupStudentListView(views.APIView):
    """
    API endpoint to show all the users for the given group
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            requested_group = self.request.data["group"]

            list_of_students = ProfileModel.objects.filter(
                student_group__title=requested_group
            )
            result = dict()
            for number, student in enumerate(list_of_students):
                result[number+1] = ProfileSerializer(student).data

            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response({"UnAuth": "Current user is not active"},
                            status=status.HTTP_401_UNAUTHORIZED)


class StudentClassJournalView(views.APIView):
    """
    API endpoint that allows user to get students results for given
    student, discipline, range(default range is whole current semester)
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            todaysdate = datetime.date.today()

            current_semester = StartSemester.objects.get(
                semesterstart__lt=todaysdate,
                semesterend__gt=todaysdate
            )
            try:
                start_date = self.request.data['start_date']
            except Exception:
                start_date = current_semester.semesterstart
            try:
                end_date = self.request.data['end_date']
            except Exception:
                end_date = current_semester.semesterend

            print start_date, end_date
            student = self.request.data['student']
            discipline = self.request.data['discipline']

            journal = StudentJournalModel.objects.filter(
                student=User.objects.get(username=student),
                discipline=Disciplines.objects.get(discipline=discipline),
                date__range=[start_date, end_date]
            )
            result = dict()
            total_value = 0
            missed_classes = 0
            for number, item in enumerate(journal):
                serialized_item = StudentJournalSerializer(item).data
                result[number+1] = serialized_item
                try:
                    total_value += int(serialized_item['value'])
                except Exception:
                    missed_classes += 1
            statistics = dict()
            statistics["total_value"] = total_value
            statistics["missed_classes"] = missed_classes
            statistics["number_of_classes"] = len(journal)

            result['stats'] = statistics

            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response({"UnAuth": "Current user is not active"},
                            status=status.HTTP_401_UNAUTHORIZED)


class ListOfDisciplinesView(APIView):
    """
    API endpoint that allows student user to check
    what classes he/she has during current semester
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
            student_group = ProfileModel.objects.get(
                user=user
            ).student_group

            disciplines = Para.objects.filter(
                semester=current_semester,
                para_group=student_group
            ).values_list('para_subject__discipline', flat=True).distinct()
            result = dict()
            for number, discipline in enumerate(disciplines):
                result[number + 1] = discipline
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response({"Authorization": "This is not an active user"},
                            status=status.HTTP_401_UNAUTHORIZED)
