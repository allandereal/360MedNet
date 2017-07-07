from django import forms
from django.contrib.auth.models import User
from material.base import Layout, Row, Fieldset
from invitation.models import Invitation, FriendInvitation
from userprofile.models import Doctor


class MedicInvitationForm(forms.ModelForm):
    name = forms.CharField(label='Invitee Name')
    organization = forms.CharField(label='Invitee Organization')
    email = forms.EmailField(label='Invitee Email')

    class Meta:
        model = Invitation
        fields = ('name', 'organization', 'email')


class FriendInvitationForm(forms.ModelForm):
    name = forms.CharField(label='Invitee Name')
    email = forms.EmailField(label='Invitee Email')

    class Meta:
        model = FriendInvitation
        fields = ('name', 'email')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    username = forms.CharField(help_text=False)
    email = forms.EmailField(label="Email Address")

    layout = Layout(Row('email', 'username', 'password')

                    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class DoctorForm(forms.ModelForm):
    layout = Layout(Fieldset('Personal details',
                             'profession', 'specialization', 'country'
                             ))

    class Meta:
        model = Doctor
        fields = ('first_name', 'last_name', 'profession', 'specialization', 'country')


def invitation_code_exists(value):
    invitee = Invitation.objects.filter(code=value).exists()
    if not invitee:
        raise forms.ValidationError("The invitation code provided does not exist. Please verify the code you have "
                                    "entered with the one sent to your email")


class RegistrationForm1(forms.ModelForm):
    invitation_code = forms.CharField(max_length=17, validators=[invitation_code_exists])

    class Meta:
        model = Doctor
        fields = ('first_name', 'last_name', 'invitation_code')


class RegistrationForm2(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    username = forms.CharField(help_text=False)
    email = forms.EmailField(label="Email Address")
    layout = Layout(email,
                    username, password

                    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email


class RegistrationForm3(forms.ModelForm):
    layout = Layout(
                    Fieldset('Medical details',
                             'profession', 'specialization', 'country'
                             ))

    class Meta:
        model = Doctor
        fields = ('profession', 'specialization', 'country')