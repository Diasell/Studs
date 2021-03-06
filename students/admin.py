from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import (
    ProfileModel,
    StudentJournalModel
)


# Define an inline admin descriptor for Profile model
# which acts a bit like a singleton
class ProfileModelInline(admin.StackedInline):
    model = ProfileModel
    can_delete = False
    verbose_name_plural = 'PROFILE INFO'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileModelInline,)


class StudentJournalModelAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'discipline', 'get_faculty', 'date']
    list_filter = ['date', 'is_module', 'discipline']
    search_fields = ['student__first_name',
                     'student__last_name',]
    def get_faculty(self, obj):
        return obj.para_number.faculty
    get_faculty.short_description = "Faculty"


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(StudentJournalModel, StudentJournalModelAdmin)
