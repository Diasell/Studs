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
from .routers import router



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include(router.urls)),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # POST/PUT STUDENT JOURNAL ITEM (PROFESSORS ONLY)
    #url(r'^api/v1/post_st_journal/$', apiv1p.StudentJournalInstanceView.as_view(), name='Journal'),

    # GET GROUPS THAT PROFESSOR IS TEACHING IN THIS SEMESTER
    #url(r'^api/v1/get_teaching_groups/$', apiv1p.GroupsListView.as_view(), name='GroupsListForProfessor'),
    url(r'^docs/', include('rest_framework_docs.urls')),

]

if DEBUG:
    # serve files from media folder
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$','django.views.static.serve',
            {'document_root': MEDIA_ROOT}))