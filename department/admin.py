from django.contrib import admin
from .models import (
    DepartmentModel,
    StudentGroupModel,
    Disciplines,
    Para,
    ParaTime,
    Rooms,
    StartSemester
)


class ParaModelAdmin(admin.ModelAdmin):
    list_display = [
        "para_subject",
        "para_professor",
        "para_room",
        "para_group",
        "para_day"
    ]
    list_filter = [
        "para_group",
        "para_day",
        "para_number",
        "week_type",
        "semester"
    ]
    search_fields = [
        "para_subject__discipline",
        "para_professor__user__first_name",
        "para_professor__user__last_name"
    ]


class RoomsModelAdmin(admin.ModelAdmin):
    list_display = ["faculty", "room"]
    list_filter = ["faculty__title", ]
    search_fields = ["room", ]


class DepartmentModelAdmin(admin.ModelAdmin):
    list_display = ["title", "faculty"]
    list_filter = ["faculty__title", ]
    search_fields = ["title"]


class ParaTimeModelAdmin(admin.ModelAdmin):
    list_display = ["__unicode__", "faculty"]
    list_filter = ["faculty__title", ]
    search_fields = ["para_position"]


class DisciplinesModelAdmin(admin.ModelAdmin):
    list_display = ["__unicode__"]
    search_fields = ["discipline"]


class StartSemesterModelAdmin(admin.ModelAdmin):
    list_display = ["__unicode__", "semesterstart", 'semesterend']
    list_filter = ["semesterstart", 'semesterend', 'title']


class StudentGroupModelAdmin(admin.ModelAdmin):
    list_display = ["__unicode__", "get_faculty", "department"]
    list_filter = ["department__faculty", "department"]
    search_fields = ["title"]

    def get_faculty(self, obj):
        return obj.department.faculty.title
    get_faculty.short_description = 'Faculty'

# Register your models here.
admin.site.register(DepartmentModel, DepartmentModelAdmin)
admin.site.register(StudentGroupModel, StudentGroupModelAdmin)
admin.site.register(Disciplines, DisciplinesModelAdmin)
admin.site.register(Rooms, RoomsModelAdmin)
admin.site.register(ParaTime, ParaTimeModelAdmin)
admin.site.register(Para, ParaModelAdmin)
admin.site.register(StartSemester, StartSemesterModelAdmin)
