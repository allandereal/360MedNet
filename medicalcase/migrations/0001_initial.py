# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-11 04:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userprofile', '0006_auto_20170510_1745'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_comments', to='userprofile.Doctor')),
            ],
        ),
        migrations.CreateModel(
            name='MedicalCase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('chief_complaint', models.CharField(max_length=200)),
                ('patient_age', models.CharField(max_length=200)),
                ('patient_gender', models.CharField(choices=[('Female', 'Female'), ('Male', 'Male')], max_length=6)),
                ('patient_country_of_origin', models.CharField(max_length=200)),
                ('history_of_present_illness', models.TextField()),
                ('medical_history', models.TextField()),
                ('surgical_history', models.TextField()),
                ('social_history', models.TextField()),
                ('family_history', models.TextField()),
                ('allergies', models.TextField()),
                ('medications', models.TextField()),
                ('review_of_systems', models.TextField()),
                ('physical_examination', models.TextField()),
                ('diagnostic_tests', models.TextField()),
                ('medical_case_category', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='userprofile.Doctor')),
            ],
        ),
        migrations.CreateModel(
            name='MedicalCaseCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='General Medicine ', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diagnotic_image', models.ImageField(blank=True, null=True, upload_to='medical_cases')),
                ('medical_case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medicalcase.MedicalCase')),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply_content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_replies', to='userprofile.Doctor')),
                ('medical_case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medicalcase.MedicalCase')),
                ('parent_comment_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medicalcase.Comment')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='medical_case',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medicalcase.MedicalCase'),
        ),
    ]