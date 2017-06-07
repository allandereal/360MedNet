from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .forms import MedicInvitationForm, FriendInvitationForm
from .models import Invitation, FriendInvitation
from django.contrib.auth.models import User
from userprofile.forms import DoctorForm, UserForm
from django.contrib import messages


def invite_user(request):
    if request.method == 'POST':
        form = MedicInvitationForm(request.POST)
        if form.is_valid():

            invitation = Invitation(
                name=form.cleaned_data['name'],
                organization=form.cleaned_data['organization'],
                email=form.cleaned_data['email'],
                code=User.objects.make_random_password(20)
            )
            if invitation.email and not User.objects.filter(email=invitation.email).exists():
                invitation.save()
                invitation.send_invite()
                messages.success(request, 'Invitation sent')
            else:
                messages.error(request, 'Invitation not sent, email already registered with 360MedNet')
    else:
        form = MedicInvitationForm()

    return render(request, 'invitation/user_invite.html', {'form': form})


@login_required
def invite_friend(request):
    if request.method == 'POST':
        form = FriendInvitationForm(request.POST)
        if form.is_valid():

            friend_invitation = FriendInvitation(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                code=User.objects.make_random_password(20),
                sender=request.user
            )
            if friend_invitation.email and not User.objects.filter(email=friend_invitation.email).exists():
                friend_invitation.save()
                friend_invitation.send_invite()
                messages.success(request, 'Invitation sent')
            else:
                messages.error(request, 'Invitation not sent, email already registered with 360MedNet')
    else:
        form = FriendInvitationForm()

    return render(request, 'invitation/friend_invite.html', {'form': form})


def join(request, code):
    invitation = get_object_or_404(Invitation, code__exact=code)
    request.session['invitation'] = invitation.id
    return HttpResponseRedirect('/register_medic/')


def join_friend_invite(request, code):
    friend_invitation = get_object_or_404(FriendInvitation, code__exact=code)
    request.session['friend_invitation'] = friend_invitation.id
    return HttpResponseRedirect('/register_medic/')


def register_invited_user(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        doctor_form = DoctorForm(data=request.POST)
        if user_form.is_valid() and doctor_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            doctor = doctor_form.save(commit=False)
            doctor.verification_status = True
            doctor.user = user
            doctor.save()
            FriendInvitation.objects.filter(email=user_form.email).update(accepted=True)
            registered = True

        else:
            print (user_form.errors, doctor_form.errors)

    else:
        user_form = UserForm()
        doctor_form = DoctorForm()

    return render(request, 'userprofile/register.html', locals())
