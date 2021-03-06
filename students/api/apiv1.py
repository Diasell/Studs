import json, requests, datetime


from ..util import (
    group_year,
    for_ios_format,
    is_valid_image,
    get_weektype
)
from rest_framework import status, views

from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate

from rest_framework.authentication import (
    TokenAuthentication,
    BasicAuthentication,
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token


from students.api.serializers import (
    UserSerializer,
    GroupSerializer,
    ProfileSerializer,
    ParaSerializer,
)
from docs_serializer import (
    RegisterViewSerializer,
    LoginViewSerializer,
    AuthorizationSerializer,
    GroupStudentsSerializer,
    GetStJournalSerializer

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
    FacultyModel,
    DepartmentModel
)


class LoginAPIView(APIView):
    """
    API that allows users login and get unique Token.
    """
    authentication_classes = (BasicAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = LoginViewSerializer

    def post(self, request, format=None):
        username = request.data["username"]
        password = request.data["password"]

        account = authenticate(username=username, password=password)

        if account is not None:
            if account.is_active:
                token = Token.objects.get_or_create(user=account)[0]
                user = User.objects.get(username=username)
                profile =ProfileSerializer(user.profilemodel).data
                result = dict()
                for key in profile:
                    result[key] = profile[key]
                result['Authorization'] = "Token %s" % token
                return Response(result, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Username/password combination is invalid'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )


class RegisterAPIView(APIView):
    """
    API that allows users to register a new account.
    """
    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class =  RegisterViewSerializer

    def post(self, request, format=None):
        # obligatory fields
        username = request.data["username"]
        password = request.data["password"]
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        c_password = request.data['confirm_password']
        birthday = request.data['birthday']
        group_title = request.data['group_title']
        group_started = request.data['group_started']
        faculty = request.data['faculty']
        email = request.data['email']

        if len(request.FILES) != 0:
            photo_flag = True
            photo = request.FILES['photo']
        else:
            photo_flag = False

        faculty = FacultyModel.objects.filter(title=faculty)
        user_group = StudentGroupModel.objects.filter(
            title=group_title,
            date_started=group_started
        )
        # validation user input
        if photo_flag:
            if photo.size > (2048*1024):
                return Response(
                    {'Failed': 'image size is greater than 2MB'},
                    status=status.HTTP_403_FORBIDDEN
                )
            try:
                is_valid_image(photo)
            except Exception:
                return Response({
                    'Failed': "attachment format is not supported"},
                    status=status.HTTP_403_FORBIDDEN
                )
        if User.objects.filter(username=username):
            return Response({
                'Failed': "username is already taken"},
                status=status.HTTP_403_FORBIDDEN
            )
        if User.objects.filter(email=email):
            return Response({
                'Failed': "email is already taken"},
                status=status.HTTP_403_FORBIDDEN
            )
        if password != c_password:
            return Response({
                'Failed': "passwords doesn't match"},
                status=status.HTTP_403_FORBIDDEN
            )
        if not faculty:
            return Response({
                'Failed': "user faculty is not valid"},
                status=status.HTTP_403_FORBIDDEN
            )
        if not user_group:
            return Response({
                'Failed': "user group is not valid"},
                status=status.HTTP_403_FORBIDDEN
            )
        serialized = UserSerializer(data=request.data).is_valid()

        if serialized:
                new_user = User.objects.create_user(
                    username = username,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    email=email
                )
                new_user.save()
                if photo_flag:
                    new_user_profile = ProfileModel(
                        user=new_user,
                        is_student=True,
                        student_group=user_group[0],
                        faculty=faculty[0],
                        started_date=group_started,
                        birthday=birthday,
                        photo=photo
                    )
                else:
                    new_user_profile = ProfileModel(
                        user=new_user,
                        is_student=True,
                        student_group=user_group[0],
                        faculty=faculty[0],
                        started_date=group_started,
                        birthday=birthday
                    )
                new_user_profile.save()

                token = Token.objects.get_or_create(user=new_user)[0]

                response = dict()
                response['Authorization'] = "Token %s" % token
                response['full_name'] = new_user.get_full_name()
                response['email'] = new_user.email
                response['group'] = new_user_profile.student_group.title
                response['faculty'] = new_user_profile.faculty.title
                if photo_flag:
                    response['photo'] = photo

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
    API that returns JSON with schedule for user.
    User can be either student or professor.
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    serializer_class = AuthorizationSerializer

    def get(self, request, format=None):
        user = request.user
        todaysdate = datetime.date.today()
        weektype = get_weektype(todaysdate)
        current_weekday = datetime.date.today().weekday()  # integer 0-monday .. 6-Sunday
        today = WorkingDay.objects.get(dayoftheweeknumber=current_weekday)
        if user.is_active:
            current_semester = StartSemester.objects.get(
                semesterstart__lt=todaysdate,
                semesterend__gt=todaysdate
            )
            if ProfileModel.objects.get(user=user).is_student:
                student_group = ProfileModel.objects.get(user=user).student_group

                classes_for_today = Para.objects.filter(
                    para_group=student_group,
                    para_day=today,
                    week_type=weektype,
                    semester=current_semester
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
    serializer_class = AuthorizationSerializer

    def get(self, request, format=None):
        user = request.user
        todaysdate = datetime.date.today()
        weektype = get_weektype(todaysdate)
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        result = dict()
        if user.is_active:
            current_semester = StartSemester.objects.get(
                semesterstart__lt=todaysdate,
                semesterend__gt=todaysdate
            )
            if ProfileModel.objects.get(user=user).is_student:
                student_group = ProfileModel.objects.get(user=user).student_group

                for day in range(0, 5):
                    classes = Para.objects.filter(
                        para_group=student_group,
                        para_day__dayoftheweeknumber=day,
                        week_type=weektype,
                        semester = current_semester
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
                        week_type=weektype,
                        semester=current_semester
                    )

                    day_js = dict()
                    for i, para in enumerate(classes):
                        day_js["para_%s" % i] = ParaSerializer(para).data

                    result["%s" % days[day]] = day_js
                return Response(result, status=status.HTTP_200_OK)
        else:
            return Response({"UnAuth": "Current user is not active"},
                            status=status.HTTP_401_UNAUTHORIZED)


class NextWeeklyScheduleView(views.APIView):
    """
    API endpoint to get user schedule for next week
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = AuthorizationSerializer

    def get(self, request, format=None):
        user = request.user
        todaysdate = datetime.date.today()
        weektype = not get_weektype(todaysdate)
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        result = dict()
        if user.is_active:
            current_semester = StartSemester.objects.get(
                semesterstart__lt=todaysdate,
                semesterend__gt=todaysdate
            )
            if ProfileModel.objects.get(user=user).is_student:
                student_group = ProfileModel.objects.get(user=user).student_group

                for day in range(0, 5):
                    classes = Para.objects.filter(
                        para_group=student_group,
                        para_day__dayoftheweeknumber=day,
                        week_type=weektype,
                        semester=current_semester,
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
                        week_type=weektype,
                        semester=current_semester
                    )

                    day_js = dict()
                    for i, para in enumerate(classes):
                        day_js["para_%s" % ParaSerializer(para).data['para_number']] = ParaSerializer(para).data

                    result["%s" % days[day]] = day_js
                return Response(result, status=status.HTTP_200_OK)
        else:
            return Response({"UnAuth": "Current user is not active"},
                            status=status.HTTP_401_UNAUTHORIZED)


class GroupStudentListView(views.APIView):
    """
    API endpoint to show all the students for the given group
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    serializer_class = AuthorizationSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            requested_group = user.profilemodel.student_group
            list_of_students = ProfileModel.objects.filter(
                student_group=requested_group
            )
            result = []
            for student in list_of_students:
                stud_dict = dict()
                temp = ProfileSerializer(student).data
                for key in temp:
                    stud_dict[key] = temp[key]
                result.append(stud_dict)
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
    serializer_class = GetStJournalSerializer

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

            discipline = self.request.data['discipline']

            journal = StudentJournalModel.objects.filter(
                student=user,
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
    serializer_class = AuthorizationSerializer

    def get(self, request):
        user = request.user
        if user.is_active:
            todaysdate = datetime.date.today()

            current_semester = StartSemester.objects.get(
                semesterstart__lt=todaysdate,
                semesterend__gt=todaysdate
            )
            student_group = user.profilemodel.student_group

            disciplines = Para.objects.filter(
                semester=current_semester,
                para_group=student_group
            ).values_list('para_subject__discipline', flat=True).distinct()
            items = list(disciplines)
            items = sorted(items)
            response = []

            for discipline in items:
                result = dict()
                result['para'] = discipline
                para = Para.objects.filter(
                    semester=current_semester,
                    para_group=student_group,
                    para_subject__discipline=discipline
                )[0]
                result['proffesor'] = para.para_professor.user.get_full_name()
                result['room'] = '605'
                try:
                    result['photo'] = para.para_professor.photo.url
                except ValueError:
                    result['photo'] = ''
                response.append(result)

            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({"Authorization": "This is not an active user"},
                            status=status.HTTP_401_UNAUTHORIZED)


class ListFacultyView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        response = dict()
        fac_list = FacultyModel.objects.all()
        for faculty in fac_list:
            groups = []
            dep_list = DepartmentModel.objects.filter(
                faculty=faculty
            )
            for department in dep_list:
                groups_list = StudentGroupModel.objects.filter(
                    department=department
                )
                for group in groups_list:
                    groups.append([group.title,
                                   group.date_started,
                                   group_year(group.date_started)])
            response[faculty.title] = groups

        return Response(for_ios_format(response), status=status.HTTP_200_OK)


class TestChatBotView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        data = request.data
        chat_id = data['message']['chat']['id']
        text = data['message']['text']

        if text == '/schedule':
            user = User.objects.get(username='380939009002')
            todaysdate = datetime.date.today()
            weektype = get_weektype(todaysdate)
            current_weekday = datetime.date.today().weekday()  # integer 0-monday .. 6-Sunday
            today = WorkingDay.objects.get(dayoftheweeknumber=current_weekday)
            if user.is_active:
                current_semester = StartSemester.objects.get(
                    semesterstart__lt=todaysdate,
                    semesterend__gt=todaysdate
                )
                if ProfileModel.objects.get(user=user).is_student:
                    student_group = ProfileModel.objects.get(user=user).student_group

                    classes_for_today = Para.objects.filter(
                        para_group=student_group,
                        para_day=today,
                        week_type=weektype,
                        semester=current_semester
                    )
                    result = ''
                    for i, para in enumerate(classes_for_today):
                        result += ParaSerializer(para).data['para_number'] + ' : ' + ParaSerializer(para).data['discipline']+ "\n"
                    a = {}
                    a["chat_id"] = chat_id
                    a['text'] = result
                    req = requests.post('https://api.telegram.org/bot289647729:AAENTWQjxU_JMOxnaEqffkwKqjhwV3NWHmU/sendMessage', a)
        else:
            a = {}
            a["chat_id"] = chat_id
            a['text'] = "commands:\n/schedule" + '\n' + 'chat_id: ' + str(chat_id)
            req = requests.post('https://api.telegram.org/bot289647729:AAENTWQjxU_JMOxnaEqffkwKqjhwV3NWHmU/sendMessage',a)

        return Response(req.json(), status=req.status_code)