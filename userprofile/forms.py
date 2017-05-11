from django import forms
from django.contrib.auth.models import User
from material.base import Layout, Row, Fieldset
from userprofile.models import Doctor, SocialSite


class VerifyForm(forms.Form):
    registration_number = forms.CharField(required=False)
    surname = forms.CharField(required=False)
    other_name = forms.CharField(required=False)

    layout = Layout(
        Row('registration_number', 'surname', 'other_name')
    )


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    username = forms.CharField(help_text=False)
    email = forms.EmailField(label="Email Address")

    layout = Layout('email', 'username', 'password'

                    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class DoctorForm(forms.ModelForm):
    layout = Layout(Fieldset('Personal details',
                    Row('first_name', 'last_name'),
                    'qualification', 'profession', 'specialization', 'country'
                    ))

    class Meta:
        model = Doctor
        fields = ('first_name', 'last_name', 'qualification', 'profession', 'specialization', 'country')


class SocialSiteForm(forms.ModelForm):
    class Meta:
        model = SocialSite
        fields = ('doctor', 'social_site', 'username')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ('first_name', 'middle_name', 'last_name', 'gender', 'date_of_birth', 'qualification', 'profession',
                  'specialization', 'country', 'city', 'year_of_first_medical_certification', 'mobile_number',
                  'about_me', 'hospital', 'work_number', 'avatar')
