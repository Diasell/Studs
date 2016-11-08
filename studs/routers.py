from django.conf.urls import url

from students.util import HybridRouter
from students.api import apiv1 as apiv1s
from professors.api import  apiv1 as apiv1p
# from blog.api import apiv1 as apiv1b


router = HybridRouter()

# viewsets:
#router.register(r'App Users', apiv1s.UserViewSet)
#router.register(r'App Permission Groups', apiv1s.GroupViewSet)
#router.register(r'Students', apiv1s.StudentViewSet)
#router.register(r'BLOG', apiv1b.BlogViewSet)

# APIViews:
router.add_api_view("User Login view",
                    url(r'^auth/login/$',
                        apiv1s.LoginAPIView.as_view(),
                        name='login-view'))
router.add_api_view("User REGISTRATION",
                    url(r'^auth/register/$',
                    apiv1s.RegisterAPIView.as_view(),
                    name='register-view'))
router.add_api_view("User Schedule for Today",
                    url(r'^get_user_schedule/$',
                        apiv1s.TodayScheduleView.as_view(),
                        name='today-schedule-view'))
router.add_api_view("User Schedule for current week",
                   url(r'^get_user_weekly_schedule/$',
                       apiv1s.WeeklyScheduleView.as_view(),
                       name='weekly-schedule-view'))
router.add_api_view("User Schedule for NEXT week",
                    url(r'^get_user_next_week_schedule/$',
                        apiv1s.NextWeeklyScheduleView.as_view(),
                        name='next-week-schedule-view'))
router.add_api_view("Show all the students for the given group",
                   url(r'^get_students_group_list/$',
                       apiv1s.GroupStudentListView.as_view(),
                       name='list-group_students-view'))
router.add_api_view("Show student discipline results by date range",
                    url(r'^get_st_dsp_result/$',
                        apiv1s.StudentClassJournalView.as_view(),
                        name='student-results-view'))
router.add_api_view("Get student classes for semester",
                    url(r'^get_students_disciplines/$',
                        apiv1s.ListOfDisciplinesView.as_view(),
                        name='student-disciplines-view'))
router.add_api_view("Get Faculty group structure",
                    url(r'^get_faculties_structure/$',
                        apiv1s.ListFacultyView.as_view(),
                        name='faculty-structure-view'))
router.add_api_view("Add\update student journal",
                    url(r'^post_st_journal/$',
                        apiv1p.StudentJournalInstanceView.as_view(),
                        name='journal-create/update-view'))
router.add_api_view("Get current groups that professor is teaching",
                    url(r'^get_teaching_groups/$',
                        apiv1p.GroupsListView.as_view(),
                        name='prof-groups-view'))
# router.add_api_view("Add Comment to Blog Item",
#                     url(r'^add_comment/$',
#                     apiv1b.AddCommentView.as_view(),
#                     name='add-comment'))
