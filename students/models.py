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


class ProfileModel(models.Model):
    """
    Students model
    """

    user = models.OneToOneField(User, primary_key=True)

    is_student = models.BooleanField(
        verbose_name=u"Student",
        default=True,
    )

    is_professor = models.BooleanField(
        verbose_name=u"Professor",
        default=False,
    )

    is_staff = models.BooleanField(
        verbose_name="Staff Member",
        default=False
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
        null=True)

    def __unicode__(self):
        if self.is_student:
            return u"Student: %s" % self.user.get_full_name()
        elif self.is_professor:
            return u"Professor: %s" % self.user.get_full_name()
        else:
            return u"Staff Member: %s" % self.user.get_full_name()


class StudentJournalModel(models.Model):

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
        return u"%s, %s, %s" % (self.date, self.discipline, self.student.get_full_name())