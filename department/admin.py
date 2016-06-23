from django.contrib import admin
from .models import DepartmentModel, FacultyModel, StudentGroupModel
# Register your models here.
admin.site.register(DepartmentModel)
admin.site.register(FacultyModel)
admin.site.register(StudentGroupModel)
