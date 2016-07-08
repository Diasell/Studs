from __future__ import unicode_literals
from django.db import models


class FacultyModel(models.Model):
    """
    Faculty Model
    """

    class Meta(object):
        verbose_name = u"Faculty"
        verbose_name_plural = u"Faculties"

    title = models.CharField(
        max_length=256,
        blank=True,
        verbose_name=u"Faculty Title",
    )

    dean = models.ForeignKey(
        'students.ProfileModel',
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

    faculty = models.ForeignKey(
        'FacultyModel',
        verbose_name=u"Faculty",
    )

    title = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Department Title",
    )

    leader = models.ForeignKey(
        'students.ProfileModel',
        verbose_name=u"Head of Department",
        blank=True,
        null=True,
    )

    def __unicode__(self):
        return u"%s" % self.title


class Rooms(models.Model):
    """
    model for that saves all rooms
    """

    class Meta(object):

        verbose_name = u"Room"
        verbose_name_plural = u"Rooms"

    room = models.CharField(
        verbose_name=u"Room",
        blank=False,
        max_length=10)

    def __unicode__(self):
        return u"%s" % self.room


class StudentGroupModel(models.Model):
    """
    Students Group Model
    """

    class Meta(object):
        verbose_name = u"Student Group"
        verbose_name_plural = u"Student Groups"

    department = models.ForeignKey(
        'DepartmentModel',
        verbose_name=u"Department",
    )

    title = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Group Title"
    )

    leader = models.ForeignKey(
        'students.ProfileModel',
        verbose_name=u"Leader",
        related_name='group',
        blank=True,
        null=True,
    )

    mentor = models.ForeignKey(
        'students.ProfileModel',
        verbose_name=u"Mentor",
        blank=True,
        null=True,
    )

    date_started = models.DateField(
        verbose_name=u"Started date"
    )

    def __unicode__(self):
        return u"%s" % self.title


class Disciplines(models.Model):
    """
    model for that saves all disciplines
    """

    class Meta(object):

        verbose_name = u"Discipline"
        verbose_name_plural = u"Disciplines"

    discipline = models.CharField(
        verbose_name=u"Discipline",
        blank=False,
        max_length=255)

    def __unicode__(self):
        return u"%s" % self.discipline


class WorkingDay(models.Model):

    class Meta(object):
        verbose_name = u"Day"
        verbose_name_plural = u"Days"

    dayoftheweek = models.CharField(max_length=50, blank=True, null=True)
    dayoftheweeknumber = models.IntegerField(
        blank=True,
        null=True
    )

    def __unicode__(self):
        return u"%s" % self.dayoftheweek


class ParaTime(models.Model):

    class Meta(object):
        verbose_name = u"Class schedule"
        verbose_name_plural = u"Class schedule"

    para_starttime = models.TimeField(
        blank=True,
        null=True,
        verbose_name=u"Starts at")

    para_endtime = models.TimeField(
        blank=True,
        null=True,
        verbose_name=u"Ends"
    )
    para_position = models.IntegerField(
        blank=True,
        null=True,
        default=0,
        verbose_name=u"Class order"
    )

    def __unicode__(self):
        return u"%s: %s-%s" % (self.para_position, self.para_starttime, self.para_endtime)


class Para(models.Model):

    class Meta(object):
        verbose_name = u"Class"
        verbose_name_plural = u"Classes"

    para_subject = models.ForeignKey(
        'Disciplines',
        blank=True,
        null=True,
        verbose_name=u"Discipline"
    )
    para_room = models.ForeignKey(
        'Rooms',
        blank=True,
        null=True,
        verbose_name=u"Room"
    )
    para_professor = models.ForeignKey(
        'students.ProfileModel',
        blank=True,
        null=True,
        verbose_name=u"Professor"
    )
    para_number = models.ForeignKey(
        'ParaTime',
        blank=True,
        null=True,
        verbose_name=u"Class Starts/Ends"
    )
    para_day = models.ForeignKey(
        WorkingDay,
        blank=True,
        null=True,
        verbose_name=u"Working day")

    para_group = models.ForeignKey(
        'StudentGroupModel',
        blank=True,
        null=True,
        verbose_name=u"Student Group"
    )
    week_type = models.BooleanField(
        default=True,
        verbose_name=u"Is week even"
    )
    semester = models.ForeignKey(
        'StartSemester',
        blank=True,
        verbose_name=u"Semester"
    )


    def __unicode__(self):
        return u"%s %s" % (self.para_subject, self.para_room)


class StartSemester(models.Model):

    class Meta(object):
        verbose_name = u"Semester schedule"
        verbose_name_plural = u"Semester's schedule"

    title = models.CharField(max_length=255,
                             blank=False,
                             null=True,
                             default=u"1st Semester",
                             verbose_name=u"Semester")
    semesterstart = models.DateField(verbose_name=u"Start at")
    semesterend = models.DateField(verbose_name=u"Ends")

    def __unicode__(self):
        return u"%s" % self.title
