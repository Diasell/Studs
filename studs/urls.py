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
from django.conf.urls import url, include
from django.contrib import admin

from rest_framework import routers
from students.api import apiv1 as apiv1s
from professors.api import  apiv1 as apiv1p


router = routers.DefaultRouter()
router.register(r'users', apiv1s.UserViewSet)
router.register(r'groups', apiv1s.GroupViewSet)
router.register(r'students', apiv1s.StudentViewSet)
router.register(r'journal', apiv1p.JournalViewSet)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # API LOGIN FOR USER TO GET TOKEN
    url(r'^api/v1/auth/login/', apiv1s.LoginAPIView.as_view(), name='login'),
    # API GET USER SCHEDULE FOR TODAY
    url(r'^api/v1/get_user_schedule/$', apiv1s.StudentTodayScheduleView.as_view(), name='StudentTodaySchedule'),
    # API GET USER SCHEDULE FOR CURRENT WEEK
    url(r'^api/v1/get_user_weekly_schedule/$', apiv1s.StudentWeekScheduleView.as_view(), name='StudentWeeklySchedule'),
    # API GET STUDENT GROUP LIST FOR GIVEN GROUP
    url(r'^api/v1/get_students_group_list/$', apiv1s.GroupStudentListView.as_view(), name='StudentsGroupList'),
    # POST/PUT STUDENT JOURNAL ITEM (PROFESSORS ONLY)
    url(r'^api/v1/post_st_journal/$', apiv1p.StudentJournalInstanceView.as_view(), name='Journal'),
    # GET STUDENT DISCIPLINE RESULT BY DATA RANGE
    url(r'^api/v1/get_st_dsp_result/$', apiv1s.StudentClassJournalView.as_view(), name='Journal1'),

]
