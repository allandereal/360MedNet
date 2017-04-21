import os
from django.db import models
from django.contrib.auth.models import User
import csv
from django.core.files.storage import default_storage
from PIL import Image


class Doctor(models.Model):
    user = models.OneToOneField(User)
    GENDER = (('Female', 'Female'), ('Male', 'Male'))
    first_name = models.CharField(max_length=100, blank=False, null=False)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    gender = models.CharField(max_length=6, choices=GENDER)
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    qualification = models.CharField(max_length=100, blank=False, null=False)
    profession = models.CharField(max_length=100, blank=False, null=False)
    specialization = models.CharField(max_length=100, blank=False, null=False)
    year_of_first_medical_certification = models.CharField(max_length=4)
    mobile_number = models.CharField(max_length=30, blank=True, null=True)
    about_me = models.TextField()
    country = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    hospital = models.CharField(max_length=30, blank=True, null=True)
    work_number = models.CharField(max_length=30, blank=True, null=True)
    avatar = models.ImageField(upload_to=None, height_field=None, width_field=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return ' %s %s' % (self.first_name, self.last_name)


class SocialSite(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    facebook = models.CharField(max_length=100, blank=True, null=True)
    linkedIn = models.CharField(max_length=100, blank=True, null=True)
    twitter = models.CharField(max_length=100, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)

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
            return str(csv_file)
        else:
            print("All files synced")

    def __str__(self):
        return str(self.file)


class Medic(models.Model):
    reg_number = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    other_name = models.CharField(max_length=100)
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
        with default_storage.open(os.path.join(str(csv_file)), 'r') as f:
            # f = default_storage.open(os.path.join(str(csv_file)), 'r', encoding="ISO-8859-1")
            reader = csv.reader(f)
            for row in reader:
                reg_number = row[0]
                if Medic.medic_exists(reg_number):
                    Medic.objects.update(reg_number=row[0], surname=row[1], other_name=row[2],
                                         sex=row[3], employer=row[4], postal_address=row[5],
                                         first_registration=row[6],
                                         date_of_first_registration=row[7],
                                         additional_qualifications=row[8], speciality=row[9],
                                         receipt_number=row[10], serial_number=row[11]
                                         )
                    medical_practitioner = + 1
                else:
                    Medic.objects.create(reg_number=row[0], surname=row[1], other_name=row[2],
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
