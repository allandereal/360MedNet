from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import DoctorForm, UserForm, VerifyForm, SocialSiteForm
from .models import Medic, Record
from django.utils.decorators import method_decorator


def verify(request):
    form = VerifyForm(data=request.POST)
    verified = False
    if request.method == 'POST' and form.is_valid():
        registration_number = form.cleaned_data['registration_number']
        surname = form.cleaned_data['surname']
        other_name = form.cleaned_data['other_name']
        qs = Medic.objects.get(reg_number=registration_number)
        if Medic.objects.filter(reg_number=registration_number, surname=surname, other_name=other_name,
                                status=False).exists():
            return HttpResponseRedirect('/accounts/verified_registration/{}'.format(qs))
        elif Medic.objects.filter(reg_number=registration_number, surname=surname, other_name=other_name,
                                  status=True).exists():
            return HttpResponseRedirect("/accounts/login")

        else:
            return HttpResponseRedirect('/accounts/unverified_registration', {'other_name': other_name})

    return render(request, 'userprofile/verify.html', {'form': form, 'verified': verified})


def register(request, medic_id):
    qs = Medic.objects.filter(reg_number=medic_id).all()
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        doctor_form = DoctorForm(data=request.POST)
        if user_form.is_valid() and doctor_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            doctor = doctor_form.save(commit=False)
            doctor.user = user
            doctor.save()
            registered = True
            qs.update(status=True)

        else:
            print (user_form.errors, doctor_form.errors)

    else:
        user_form = UserForm()
        doctor_form = DoctorForm()

    return render(request, 'userprofile/register.html',
                  {'user_form': user_form, 'doctor_form': doctor_form, 'registered': registered, 'qs': qs})


def unverified_register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        doctor_form = DoctorForm(data=request.POST)
        if user_form.is_valid() and doctor_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            doctor = doctor_form.save(commit=False)
            doctor.user = user
            doctor.save()

            registered = True

        else:
            print (user_form.errors, doctor_form.errors)

    else:
        user_form = UserForm()
        doctor_form = DoctorForm()

    return render(request, 'userprofile/unverified_register.html',
                  {'user_form': user_form, 'doctor_form': doctor_form, 'registered': registered})


def profile(request):
    record = Record.get_record_file()
    return render(request, 'userprofile/profile.html', {'record': record})


def logout(request):
    return HttpResponseRedirect('/')
