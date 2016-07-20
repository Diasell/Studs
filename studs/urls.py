"""studs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from .settings import MEDIA_ROOT, DEBUG
from django.conf.urls import url, include, patterns
from django.contrib import admin

from rest_framework import routers
from students.api import apiv1 as apiv1s
from professors.api import  apiv1 as apiv1p
from blog.api import apiv1 as apiv1b


router = routers.DefaultRouter()
router.register(r'users', apiv1s.UserViewSet)
router.register(r'groups', apiv1s.GroupViewSet)
router.register(r'students', apiv1s.StudentViewSet)
router.register(r'blog', apiv1b.BlogViewSet)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # API LOGIN FOR USER TO GET TOKEN
    url(r'^api/v1/auth/login/', apiv1s.LoginAPIView.as_view(), name='login'),
    # API REGISTER NEW USER
    url(r'^api/v1/auth/register/', apiv1s.RegisterAPIView.as_view(), name='register'),
    # API GET USER SCHEDULE FOR TODAY
    url(r'^api/v1/get_user_schedule/$', apiv1s.TodayScheduleView.as_view(), name='TodaySchedule'),
    # API GET USER SCHEDULE FOR CURRENT WEEK
    url(r'^api/v1/get_user_weekly_schedule/$', apiv1s.WeeklyScheduleView.as_view(), name='WeeklySchedule'),
    # API GET STUDENT GROUP LIST FOR GIVEN GROUP
    url(r'^api/v1/get_students_group_list/$', apiv1s.GroupStudentListView.as_view(), name='StudentsGroupList'),
    # POST/PUT STUDENT JOURNAL ITEM (PROFESSORS ONLY)
    url(r'^api/v1/post_st_journal/$', apiv1p.StudentJournalInstanceView.as_view(), name='Journal'),
    # GET STUDENT DISCIPLINE RESULT BY DATA RANGE
    url(r'^api/v1/get_st_dsp_result/$', apiv1s.StudentClassJournalView.as_view(), name='Journal1'),
    # GET GROUPS THAT PROFESSOR IS TEACHING IN THIS SEMESTER
    url(r'^api/v1/get_teaching_groups/$', apiv1p.GroupsListView.as_view(), name='GroupsListForProfessor'),
    # GET DISCIPLINES THAT STUDENT USER IS VISITING IN THIS SEMESTER
    url(r'^api/v1/get_students_disciplines/$', apiv1s.ListOfDisciplinesView.as_view(), name='ListOfStDisciplines'),

]

if DEBUG:
    # serve files from media folder
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$','django.views.static.serve',
            {'document_root': MEDIA_ROOT}))