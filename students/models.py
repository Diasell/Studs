from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class ProfileModel(models.Model):
    """
    Students Profile model
    """

    user = models.OneToOneField(User, primary_key=True)

    is_student = models.BooleanField(
        verbose_name=u"Student",
        default=True,
    )

    is_professor = models.BooleanField(
        verbose_name=u"Professor",
        default=False,
        blank=True
    )

    is_staff = models.BooleanField(
        verbose_name="Staff Member",
        default=False,
        blank=True
    )

    started_date = models.DateField(
        auto_now_add=True,
        verbose_name=u"Started Working/Studying"
    )

    faculty = models.ForeignKey(
        'department.FacultyModel',
        verbose_name=u"Faculty",
        blank=True,
        null=True,
    )

    department = models.ForeignKey(
        'department.DepartmentModel',
        verbose_name=u"Department",
        blank=True,
        null=True,
    )

    student_group = models.ForeignKey(
        'department.StudentGroupModel',
        verbose_name=u"Group",
        blank=True,
        null=True,
    )

    middle_name = models.CharField(
        max_length=256,
        blank=True,
        verbose_name=u"Middle Name",
        default='')

    birthday = models.DateField(
        blank=True,
        verbose_name=u"Date of Birth",
        null=True)

    contact_phone = models.CharField(
        max_length=55,
        blank=True,
        verbose_name=u"Contact Phone",
        null=True,
    )

    photo = models.ImageField(
        blank=True,
        verbose_name=u"Photo",
        upload_to=user_directory_path,
        null=True)

    def __unicode__(self):
        if self.is_student:
            return u"Student: %s" % self.user.get_full_name()
        elif self.is_professor:
            return u"Professor: %s" % self.user.get_full_name()
        else:
            return u"Staff Member: %s" % self.user.get_full_name()


class StudentJournalModel(models.Model):

    class Meta(object):
        verbose_name = u"Student Journal"
        verbose_name_plural = u"Student Journal"

    value = models.CharField(
        max_length=55,
        blank=True,
        null=True,
        verbose_name="Value",
        default=''
    )
    date = models.DateField(
        verbose_name="Date"
    )
    discipline = models.ForeignKey(
        'department.Disciplines',
        verbose_name="Discipline"
    )
    para_number = models.ForeignKey(
        'department.ParaTime',
        verbose_name="Class #"
    )
    student = models.ForeignKey(
        User,
        verbose_name="Student"
    )
    is_module = models.BooleanField(
        verbose_name="Module value"
    )

    def __unicode__(self):
        return u"%s" % self.student.get_full_name()