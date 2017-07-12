# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-09 07:14
from __future__ import unicode_literals

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('medicalcase', '0005_auto_20170709_0243'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicalcase',
            name='medical_case_category',
        ),
        migrations.AddField(
            model_name='medicalcase',
            name='medical_case_category',
            field=models.ManyToManyField(to='medicalcase.MedicalCaseCategory'),
        ),
        migrations.AlterField(
            model_name='medicalcase',
            name='purpose',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('I need help!', 'I need help!'), ('I found this case interesting.', 'I found this case interesting.'), ('I need help!', 'I need help!')], max_length=56),
        ),
    ]