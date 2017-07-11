from django import forms
from django.contrib.auth.models import User
from material.base import Layout, Row, Fieldset
from userprofile.models import Doctor, SocialSite, Qualification, Medic


class VerifyForm(forms.Form):
    other_name = forms.CharField(max_length=200, label="First Name(s)")
    surname = forms.CharField(max_length=200)
    alternative_email = forms.EmailField(required=False, label="Your primary email address")
    organization = forms.CharField(required=False, label="Organization, Hostpital or Company")

    layout = Layout(
        Row('other_name', 'surname'),
        'alternative_email',
        'organization'

    )

    def clean(self):
        cleaned_data = super(VerifyForm, self).clean()
        other_name = cleaned_data.get("other_name")
        surname = cleaned_data.get("surname")

        if not Medic.objects.get(surname__iexact=surname, other_name__iexact=other_name):
            raise forms.ValidationError("%s %s does not exist in our database. Please provide your registered name as "
                                        "per on the medical license" % (other_name, surname))
        return self.cleaned_data


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(label="Email Address")

    layout = Layout(Row('email', 'password')

                    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)


class DoctorForm(forms.ModelForm):
    country = forms.CharField(label="Country of Practice")
    layout = Layout(Fieldset('Personal details',
                             Row('first_name', 'last_name'),
                             'profession', 'specialization', 'country'
                             ))

    class Meta:
        model = Doctor
        fields = ('first_name', 'last_name', 'profession', 'specialization', 'country')


class SocialSiteForm(forms.ModelForm):
    class Meta:
        model = SocialSite
        fields = ('doctor', 'social_site', 'username')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ('first_name', 'middle_name', 'last_name', 'gender', 'date_of_birth', 'profession',
                  'specialization', 'country', 'city', 'year_of_first_medical_certification', 'mobile_number',
                  'about_me', 'hospital', 'work_number', 'avatar')


class QualificationForm(forms.ModelForm):
    class Meta:
        model = Qualification
        fields = ('field_of_study', 'qualification', 'university')
