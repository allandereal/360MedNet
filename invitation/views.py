from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .forms import MedicsInvitationForm
from .models import Invitation
from django.contrib.auth.models import User
from userprofile.forms import DoctorForm, UserForm


def invite_user(request):
    if request.method == 'POST':
        form = MedicsInvitationForm(request.POST)
        if form.is_valid():
            invitation = Invitation(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                code=User.objects.make_random_password(20)
            )
            invitation.save()
            invitation.send_invite()
            return HttpResponseRedirect('/invite')
    else:
        form = MedicsInvitationForm()

    return render(request, 'invitation/user_invite.html', {'form': form})


def join(request, code):
    invitation = get_object_or_404(Invitation, code__exact=code)
    request.session['invitation'] = invitation.id
    return HttpResponseRedirect('/register_invitee/')


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
            registered = True

        else:
            print (user_form.errors, doctor_form.errors)

    else:
        user_form = UserForm()
        doctor_form = DoctorForm()

    return render(request, 'userprofile/register.html', locals())
