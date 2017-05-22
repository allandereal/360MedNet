from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import DoctorForm, UserForm, VerifyForm, SocialSiteForm
from .models import Medic, Doctor
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator


def verify(request):
    form = VerifyForm(data=request.POST)
    verified = False
    if request.method == 'POST' and form.is_valid():
        registration_number = form.cleaned_data['registration_number']
        surname = form.cleaned_data['surname']
        other_name = form.cleaned_data['other_name']
        if Medic.objects.filter(reg_number=registration_number, surname__iexact=surname, other_name__iexact=other_name,
                                status=False).exists():
            qs = Medic.objects.get(reg_number=registration_number)
            return HttpResponseRedirect('/accounts/verified_registration/{}'.format(qs))
        elif Medic.objects.filter(reg_number=registration_number, surname__iexact=surname,
                                  other_name__iexact=other_name,
                                  status=True).exists():
            return HttpResponseRedirect("/accounts/login")
        else:
            qs = {'other_name': other_name}
            return HttpResponseRedirect('/accounts/unverified_registration/', {'qs': qs})

    return render(request, 'userprofile/verify.html', {'form': form, 'verified': verified})


def register(request, reg_number):
    qs = Medic.objects.filter(reg_number=reg_number).all()
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
            qs.update(status=True)

        else:
            print (user_form.errors, doctor_form.errors)

    else:
        user_form = UserForm()
        doctor_form = DoctorForm()

    return render(request, 'userprofile/register.html', locals())


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

    return render(request, 'userprofile/unverified_register.html', locals())


# def view_profile(request):
#     user = User.objects.get(username=username)
#     return HttpResponseRedirect('/accounts/profile/{}'.format(user))


def get_profile(request, username):
    user = User.objects.get(username=username)
    read_profile = Doctor.view_profile()
    return render(request, 'userprofile/read_profile.html', {'read_profile': read_profile, 'user': user})


def logout(request):
    return HttpResponseRedirect('/')


class UpdateProfile(UpdateView):
    model = Doctor
    fields = ['first_name', 'middle_name', 'last_name', 'gender', 'date_of_birth', 'qualification', 'profession',
              'specialization', 'country', 'city', 'year_of_first_medical_certification', 'mobile_number',
              'about_me', 'hospital', 'work_number', 'avatar']

    template_name = 'userprofile/doctor_profile_update.html'
    success_url = '/accounts/profile/(?P<username>[a-zA-Z0-9]+)'


def home(request):
    return render(request, 'userprofile/home.html')
