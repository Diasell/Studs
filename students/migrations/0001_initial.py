# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-29 07:31
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
        ('department', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileModel',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('is_student', models.BooleanField(default=True, verbose_name='Student')),
                ('is_professor', models.BooleanField(default=False, verbose_name='Professor')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Staff Member')),
                ('started_date', models.DateField(auto_now_add=True, verbose_name='Started Working/Studying')),
                ('middle_name', models.CharField(blank=True, default='', max_length=256, verbose_name='Middle Name')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='Date of Birth')),
                ('contact_phone', models.CharField(blank=True, max_length=55, null=True, verbose_name='Contact Phone')),
                ('photo', models.ImageField(blank=True, null=True, upload_to=b'', verbose_name='Photo')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='department.DepartmentModel', verbose_name='Department')),
                ('faculty', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='department.FacultyModel', verbose_name='Faculty')),
                ('student_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='department.StudentGroupModel', verbose_name='Group')),
            ],
        ),
    ]
