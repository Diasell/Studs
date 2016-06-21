from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from department.models import StudentGroupModel

class StudentProfileModel(models.Model):
    """
    Students model
    """

    user = models.OneToOneField(User, primary_key=True)

    middle_name = models.CharField(
        max_length=256,
        blank=True,
        verbose_name=u"Middle Name",
        default='')

    student_group = models.ForeignKey(
        StudentGroupModel,
        verbose_name=u"Group",
        blank=False,
        null=True,
        on_delete=models.PROTECT,
    )

    birthday = models.DateField(
        blank=False,
        verbose_name=u"Date of Birth",
        null=True)

    photo = models.ImageField(
        blank=True,
        verbose_name=u"Photo",
        null=True)

    contact_phone = models.CharField(
        max_length=55,
        blank=True,
        verbose_name=u"Contact Phone",
        null=True,
    )

    def __unicode__(self):
        return u"%s, %s" % (self.user, self.student_group.title)

