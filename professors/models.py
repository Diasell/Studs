from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from department.models import DepartmentModel


class ProfessorProfileModel(models.Model):
    """
    Professor Model
    """

    user = models.OneToOneField(User, primary_key=True)

    middle_name = models.CharField(
        max_length=256,
        blank=True,
        verbose_name=u"Middle Name",
        default='',
    )

    department = models.ForeignKey(
        DepartmentModel,
        verbose_name=u"Department",
        blank=True,
        null=True,
    )

    birthday = models.DateField(
        blank=False,
        verbose_name=u"Date of Birth",
        null=True,
    )

    photo = models.ImageField(
        blank=True,
        verbose_name=u"Photo",
        null=True,
    )

    contact_phone = models.CharField(
        max_length=55,
        blank=True,
        null=True,
        verbose_name=u"Contact Phone"
    )

    started_working = models.DateField(
        a
    )

    def __unicode__(self):
        return u"%s, %s" % (self.user, self.department.title)
