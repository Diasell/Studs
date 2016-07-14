from django.contrib import admin
from .models import (
    DepartmentModel,
    FacultyModel,
    StudentGroupModel,
    Disciplines,
    Para,
    ParaTime,
    Rooms,
    WorkingDay,
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

# Register your models here.
admin.site.register(DepartmentModel)
admin.site.register(FacultyModel)
admin.site.register(StudentGroupModel)
admin.site.register(Disciplines)
admin.site.register(Rooms)
admin.site.register(ParaTime)
admin.site.register(Para, ParaModelAdmin)
admin.site.register(WorkingDay)
admin.site.register(StartSemester)