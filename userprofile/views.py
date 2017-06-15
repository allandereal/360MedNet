from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse
from .forms import DoctorForm, UserForm, VerifyForm, SocialSiteForm
from .models import Medic, Doctor
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ValidationError
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage


class EmailAuthenticationForm(AuthenticationForm):
    def clean_username(self):
        username = self.data['username']
        if '@' in username:
            try:
                username = User.objects.get(email=username).username
            except ObjectDoesNotExist:
                raise ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
        return username


def verify(request):
    form = VerifyForm(data=request.POST)
    verified = False
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        surname = form.cleaned_data['surname']
        other_name = form.cleaned_data['other_name']
        if Medic.objects.filter(email__iexact=email, surname__iexact=surname, other_name__iexact=other_name,
                                status=False).exists():
            qs = Medic.objects.get(email=email)
            return HttpResponseRedirect('/accounts/verified_registration/{}'.format(qs))
        elif Medic.objects.filter(email__iexact=email, surname__iexact=surname,
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


def get_profile(request, username):
    user = User.objects.get(username=username)
    read_profile = Doctor.objects.get(user=user)
    return render(request, 'userprofile/read_profile.html', {'read_profile': read_profile, 'user': user})


class UpdateProfile(UpdateView):
    model = Doctor
    fields = ['first_name', 'middle_name', 'last_name', 'gender', 'date_of_birth', 'qualification', 'profession',
              'specialization', 'country', 'city', 'year_of_first_medical_certification', 'mobile_number',
              'about_me', 'hospital', 'work_number', 'avatar']

    template_name = 'userprofile/doctor_profile_update.html'
    success_url = '/accounts/profile/(?P<username>[a-zA-Z0-9]+)'


class DoctorDetail(DetailView):
    model = Doctor

    def get_context_data(self, **kwargs):
        context = super(DoctorDetail, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


def home(request):
    return render(request, 'userprofile/home.html')


def signup(request):
    form = VerifyForm(data=request.POST)
    verified = False
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        surname = form.cleaned_data['surname']
        other_name = form.cleaned_data['other_name']
        if Medic.objects.filter(email=email, surname__iexact=surname, other_name__iexact=other_name,
                                status=False).exists():
            qs = Medic.objects.get(email=email)
            generate_password = User.objects.make_random_password(8)
            user = User.objects.create_user(username=surname+other_name, email=email,
                                            password=generate_password)
            doctor = Doctor.objects.create(last_name=surname, first_name=other_name, user=user)
            current_site = get_current_site(request)
            subject = 'Your account credentials on 360MedNet.'
            message = render_to_string('userprofile/activate_email.html', {
                'user': user,
                'doctor': doctor,
                'domain': current_site.domain,
                'password': generate_password

            })
            to_email = email
            email = EmailMessage(subject, message, to=[to_email])
            email.send()
            # return HttpResponse('Check your email to activate your account')
            return HttpResponseRedirect(reverse('signup_activate'))

            #return HttpResponseRedirect(reverse('url_name'))
        elif Medic.objects.filter(email=email, surname__iexact=surname,
                                  other_name__iexact=other_name,
                                  status=True).exists():
            return HttpResponseRedirect("/accounts/login")
        else:
            qs = {'other_name': other_name}
            return HttpResponseRedirect('/accounts/unverified_registration/', {'qs': qs})
    return render(request, 'userprofile/signup.html', {'form': form, 'verified': verified})


def signup_activate(request):
    return render(request, 'userprofile/signup_activate.html')


class RegisterUpdateView(UpdateView):
    model = Doctor
    fields = ['first_name', 'last_name',  'profession', 'country']

    template_name = 'userprofile/register_update.html'
    success_url = 'login'

