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

# Register your models here.
admin.site.register(DepartmentModel)
admin.site.register(FacultyModel)
admin.site.register(StudentGroupModel)
admin.site.register(Disciplines)
admin.site.register(Rooms)
admin.site.register(ParaTime)
admin.site.register(Para)
admin.site.register(WorkingDay)
admin.site.register(StartSemester)