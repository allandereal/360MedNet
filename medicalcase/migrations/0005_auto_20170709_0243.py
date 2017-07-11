# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-08 23:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicalcase', '0004_auto_20170709_0153'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created_at'], 'verbose_name_plural': 'Comments'},
        ),
        migrations.AlterModelOptions(
            name='medicalcasecategory',
            options={'ordering': ['-created_at'], 'verbose_name_plural': 'Medical Case Categories'},
        ),
        migrations.AlterModelOptions(
            name='photo',
            options={'ordering': ['-created_at'], 'verbose_name_plural': 'Photos'},
        ),
        migrations.AlterModelOptions(
            name='reply',
            options={'ordering': ['-created_at'], 'verbose_name_plural': 'Replies'},
        ),
        migrations.AlterField(
            model_name='medicalcase',
            name='patient_gender',
            field=models.CharField(choices=[('Female', 'Female'), ('Male', 'Male'), ('Others', 'Others')], default='Female', max_length=6),
        ),
    ]
