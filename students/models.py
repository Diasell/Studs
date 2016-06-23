from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


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
            return u"Student: %s, Group: %s" % (self.user, self.student_group)
        elif self.is_professor:
            return u"Professor: %s, Department: %s" % (self.user, self.department)
        else:
            return u"Staff Member: %s, Faculty: %s" % (self.user, self.faculty)