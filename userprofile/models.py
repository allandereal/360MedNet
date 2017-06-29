import os
from django.db import models
from django.contrib.auth.models import User
import csv
from django.core.files.storage import default_storage
import urllib.request
import codecs
from PIL import Image
from django.urls import reverse
import io
import requests
from contextlib import closing
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django.conf import settings


class Profession(models.Model):
    profession = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return str(self.profession)


class Specialization(models.Model):
    specialization = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return str(self.specialization)


class Doctor(models.Model):
    user = models.OneToOneField(User)
    GENDER = (('Female', 'Female'), ('Male', 'Male'))
    first_name = models.CharField(max_length=100, blank=False, null=False)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    gender = models.CharField(max_length=6, choices=GENDER)
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    #qualification = models.CharField(max_length=100, blank=True, null=True)
    profession = models.ForeignKey(Profession)
    specialization = models.ForeignKey(Specialization)
    year_of_first_medical_certification = models.CharField(max_length=4)
    mobile_number = models.CharField(max_length=30, blank=True, null=True)
    about_me = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    hospital = models.CharField(max_length=30, blank=True, null=True)
    work_number = models.CharField(max_length=30, blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars", default='avatars/none/default.jpeg', height_field=None,
                               width_field=None, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    verification_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return ' %s %s' % (self.first_name, self.last_name)

    @classmethod
    def view_profile(cls):
        return cls.objects.all()

    def get_absolute_url(self):
        return reverse('doctor-detail', kwargs={'pk': self.pk})

    def send_login_credentials(self):
        subject = 'Complete Registration on 360MedNet'
        link = 'http://%s/join/%s/' % (
            settings.SITE_HOST,
            self.code
        )
        template = get_template('invitation/invitation_email.html')
        context = Context({
            'name': self.name,
            'organization': self.organization,
            'link': link,
        })
        message = template.render(context)
        send_mail(
            subject, message,
            settings.EMAIL_HOST_USER, [self.email]
        )


class Qualification(models.Model):
    qualification = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=200)
    university = models.CharField(max_length=200)
    doctor = models.ForeignKey(Doctor)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return str(self.qualification)


class SocialSite(models.Model):
    SOCIAL_SITE = (('LinkedIn', 'LinkedIn'), ('Facebook', 'Facebook'), ('Twitter', 'Twitter'), ('Youtube', 'Youtube'))

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    social_site = models.CharField(max_length=50, choices=SOCIAL_SITE)
    username = models.CharField(max_length=100)

    def __str__(self):
        return '%s', self.doctor_id


class Record(models.Model):
    file = models.FileField(upload_to="records")
    synced = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_record_file(cls):
        if cls.objects.filter(synced=False).exists():
            csv_file = cls.objects.filter(synced=False).first().file
            Medic.create_medic(csv_file=csv_file)
        else:
            print("All files synced")

    def __str__(self):
        return str(self.file)


class Medic(models.Model):
    reg_number = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    other_name = models.CharField(max_length=100)
    email = models.EmailField()
    sex = models.CharField(max_length=1)
    employer = models.CharField(max_length=100)
    postal_address = models.CharField(max_length=100)
    first_registration = models.CharField(max_length=100)
    date_of_first_registration = models.CharField(max_length=100)
    additional_qualifications = models.TextField()
    speciality = models.CharField(max_length=100)
    receipt_number = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    status = models.BooleanField(default=False)

    @classmethod
    def create_medic(cls, csv_file):
        medical_practitioner = 0

        url = "https://360mednet.s3.amazonaws.com/%s" % csv_file
        ftpstream = urllib.request.urlopen(url)
        csvfile = csv.reader(ftpstream.read().decode('ISO-8859-1'))
        csvfile = csv.reader(url)
        # csvfile = csv.reader(io.TextIOWrapper(ftpstream))
        # with default_storage.open(os.path.join(str(csv_file)), 'rt') as f:
        #     f = default_storage.open(os.path.join(str(csv_file)), 'r')
        #     csvfile = csv.reader(f)

        for row in csvfile:
            reg_number = row[0]
            if not Medic.medic_exists(reg_number):
                Medic.objects.create(reg_number=row[0], surname=row[1], other_name=row[2],
                                     sex=row[3], employer=row[4], postal_address=row[5],
                                     first_registration=row[6],
                                     date_of_first_registration=row[7],
                                     additional_qualifications=row[8], speciality=row[9],
                                     receipt_number=row[10], serial_number=row[11]
                                     )
                medical_practitioner = + 1
            else:
                Medic.objects.filter(reg_number=row[0]).update(surname=row[1], other_name=row[2],
                                                               sex=row[3], employer=row[4], postal_address=row[5],
                                                               first_registration=row[6],
                                                               date_of_first_registration=row[7],
                                                               additional_qualifications=row[8], speciality=row[9],
                                                               receipt_number=row[10], serial_number=row[11]
                                                               )
                medical_practitioner = + 1

            Record.objects.filter(file=csv_file).update(synced=True)
        return medical_practitioner

    @classmethod
    def medic_exists(cls, reg_number):
        return cls.objects.filter(reg_number=reg_number).exists()

    def __str__(self):
        return self.reg_number
