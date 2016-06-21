from __future__ import unicode_literals

from django.db import models
from students.models import StudentProfileModel
from professors.models import ProfessorProfileModel


class FacultyModel(models.Model):
    """
    Faculty Model
    """

    class Meta(object):
        verbose_name = u"Faculty"
        verbose_name_plural = u"Faculties"

    title = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Faculty Title",
    )

    dean = models.ForeignKey(
        ProfessorProfileModel,
        verbose_name=u"Dean",
        null=True,
        blank=True,
    )

    department_address = models.CharField(
        max_length=1000,
        null=True,
        blank=True,
        verbose_name=u"Departments address",
    )

    def __unicode__(self):
        return u"%s" % self.title


class DepartmentModel(models.Model):
    """
    Department Model
    """

    class Meta(object):
        verbose_name = u"Department"
        verbose_name_plural = u"Departments"

    department = models.ForeignKey(
        FacultyModel,
        verbose_name=u"Faculty",
    )

    title = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Department Title",
    )

    leader = models.ForeignKey(
        ProfessorProfileModel,
        verbose_name=u"Head of Department",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __unicode__(self):
        return u"%s, %s" % (self.department.title, self.title)


class StudentGroupModel(models.Model):
    """
    Students Group Model
    """

    class Meta(object):
        verbose_name = u"Student Group"
        verbose_name_plural = u"Student Groups"

    department = models.ForeignKey(
        DepartmentModel,
        verbose_name=u"Department",
    )

    title = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Group Title"
    )

    leader = models.OneToOneField(
        StudentProfileModel,
        verbose_name=u"Leader",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    mentor = models.ForeignKey(
        ProfessorProfileModel,
        verbose_name=u"Mentor",
        blank=True,
        null=True,
    )

    date_started = models.DateField(
        verbose_name=u"Started date"
    )

    def __unicode__(self):
        return u"%s, %s" % (self.department.title, self.title)
