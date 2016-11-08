import datetime
from PIL import Image
from datetime import timedelta
from rest_framework import routers, views, reverse, response

from department.models import (
    StartSemester,
)


def group_year(date_started):
    """
    :param date_started: date when group was created
    :return: str that represents the course for the group
    """
    today = datetime.date.today()
    course = ((today - date_started).days / 365) + 1
    return u"%s course" % course


def for_ios_format(response):
    updated_response = dict()
    for key in response:
        group_t = dict()
        for group in response[key]:
            if group[0] not in group_t:
                course = dict()
                course[group[2]] = group[1]
                group_t[group[0]] = course
            else:
                courses = group_t[group[0]]
                courses[group[2]] = group[1]
                group_t[group[0]] = courses
        updated_response[key] = group_t
    return updated_response


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
    for semester in semesters:
        if semester.semesterstart <= date \
                and semester.semesterend >= date:
            return ifweekiseven(date, semester.semesterstart)
    return None


def is_valid_image(photo):
    """uses Pillow to check whether file is an image"""

    image = Image.open(photo)
    valid_formats = ['jpeg', 'jpg', 'png']
    if image.format.lower() in valid_formats:
        return True
    return False


class HybridRouter(routers.DefaultRouter):
    def __init__(self, *args, **kwargs):
        super(HybridRouter, self).__init__(*args, **kwargs)
        self._api_view_urls = {}

    def add_api_view(self, name, url):
        self._api_view_urls[name] = url

    def remove_api_view(self, name):
        del self._api_view_urls[name]

    @property
    def api_view_urls(self):
        ret = {}
        ret.update(self._api_view_urls)
        return ret

    def get_urls(self):
        urls = super(HybridRouter, self).get_urls()
        for api_view_key in self._api_view_urls.keys():
            urls.append(self._api_view_urls[api_view_key])
        return urls

    def get_api_root_view(self):
        # Copy the following block from Default Router
        api_root_dict = {}
        list_name = self.routes[0].name
        for prefix, viewset, basename in self.registry:
            api_root_dict[prefix] = list_name.format(basename=basename)
        api_view_urls = self._api_view_urls

        class APIRoot(views.APIView):
            _ignore_model_permissions = True

            def get(self, request, format=None):
                ret = {}
                for key, url_name in api_root_dict.items():
                    ret[key] = reverse.reverse(url_name, request=request, format=format)
                # In addition to what had been added, now add the APIView urls
                for api_view_key in api_view_urls.keys():
                    ret[api_view_key] = reverse.reverse(api_view_urls[api_view_key].name, request=request, format=format)
                return response.Response(ret)

        return APIRoot.as_view()


def format_time(str):
    x = str.replace(" ",'')
    y = x.replace('.','_')
    result = y.replace(':','_')
    return result

def custom_logger(data, user):
    """
    :param request: request.data  that comes from the clients request
    creates and saves new file with request data
    """
    path = "../media/logs/"
    time = format_time(str(datetime.datetime.now()))
    filename = path + time + '.log'
    with open(filename, "w+") as f:
        f.write(str(user) + ':' + str(data))

