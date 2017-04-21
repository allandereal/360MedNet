from django import forms
from django.contrib.auth.models import User
from userprofile.models import Doctor, SocialSite


class VerifyForm(forms.Form):
    registration_number = forms.CharField(required=True)
    surname = forms.CharField(required=True)
    other_name = forms.CharField(required=True)

    #class Meta:
        #model = Doctor
        #fields = ('first_name', 'last_name', 'middle_name')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    username = forms.CharField(help_text=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ('first_name', 'last_name', 'qualification', 'profession', 'specialization', 'country')


class SocialSiteForm(forms.ModelForm):
    class Meta:
        model = SocialSite
        fields = ('doctor', 'facebook', 'linkedIn', 'twitter', 'website')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ('first_name', 'middle_name', 'last_name', 'gender', 'date_of_birth','qualification', 'profession',
                  'specialization', 'country', 'city', 'year_of_first_medical_certification', 'mobile_number',
                  'about_me', 'hospital', 'work_number','avatar')