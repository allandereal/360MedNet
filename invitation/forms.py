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
                    Row('first_name', 'last_name'),
                    'qualification', 'profession', 'specialization', 'country'
                    ))

    class Meta:
        model = Doctor
        fields = ('first_name', 'last_name', 'qualification', 'profession', 'specialization', 'country')

