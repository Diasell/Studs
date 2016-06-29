# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-29 07:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('department', '0001_initial'),
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentgroupmodel',
            name='leader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='group', to='students.ProfileModel', verbose_name='Leader'),
        ),
        migrations.AddField(
            model_name='studentgroupmodel',
            name='mentor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='students.ProfileModel', verbose_name='Mentor'),
        ),
        migrations.AddField(
            model_name='para',
            name='para_day',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='department.WorkingDay', verbose_name='Working day'),
        ),
        migrations.AddField(
            model_name='para',
            name='para_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='department.StudentGroupModel', verbose_name='Student Group'),
        ),
        migrations.AddField(
            model_name='para',
            name='para_number',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='department.ParaTime', verbose_name='Class Starts/Ends'),
        ),
        migrations.AddField(
            model_name='para',
            name='para_professor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='students.ProfileModel', verbose_name='Professor'),
        ),
        migrations.AddField(
            model_name='para',
            name='para_room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='department.Rooms', verbose_name='Room'),
        ),
        migrations.AddField(
            model_name='para',
            name='para_subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='department.Disciplines', verbose_name='Discipline'),
        ),
        migrations.AddField(
            model_name='facultymodel',
            name='dean',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='students.ProfileModel', verbose_name='Dean'),
        ),
        migrations.AddField(
            model_name='departmentmodel',
            name='faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='department.FacultyModel', verbose_name='Faculty'),
        ),
        migrations.AddField(
            model_name='departmentmodel',
            name='leader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='students.ProfileModel', verbose_name='Head of Department'),
        ),
    ]