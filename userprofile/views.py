from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse
from .forms import DoctorForm, UserForm, VerifyForm, ProfileForm, SocialSiteForm, QualificationForm
from .models import Medic, Doctor, Qualification
from django.views.generic.edit import UpdateView, CreateView
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ValidationError
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy


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
            email = user_form.cleaned_data['email']
            password = user_form.cleaned_data['password']
            username = user_form.cleaned_data['username']
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            doctor = doctor_form.save(commit=False)
            doctor.verification_status = True
            doctor.user = user
            doctor.save()
            registered = True
            qs.update(status=True)
            current_site = get_current_site(request)
            subject = 'Welcome to 360MedNet.'
            message = render_to_string('userprofile/thank_you_signup_email.html', {
                'user': user,
                'doctor': doctor,
                'domain': current_site.domain,
                'password': password

            })
            to_email = email
            email = EmailMessage(subject, message, to=[to_email])
            email.content_subtype = "html"
            email.send()

        else:
            print(user_form.errors, doctor_form.errors)

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
            current_site = get_current_site(request)
            subject = 'Welcome to 360MedNet.'
            message = render_to_string('userprofile/thank_you_signup_email.html', {
                'user': user,
                'doctor': doctor,
                'domain': current_site.domain,
                'password': user.password

            })
            to_email = user.email
            email = EmailMessage(subject, message, to=[to_email])
            email.content_subtype = "html"
            email.send()

        else:
            print(user_form.errors, doctor_form.errors)

    else:
        user_form = UserForm()
        doctor_form = DoctorForm()

    return render(request, 'userprofile/unverified_register.html', locals())


@login_required(login_url='/login/')
def get_profile(request, username):
    user = User.objects.get(username=username)
    doctor = Doctor.objects.get(user=user)
    read_profile = Doctor.objects.get(user=user)
    read_qualification = Qualification.objects.filter(doctor=doctor).all()

    return render(request, 'userprofile/read_profile.html', {'read_profile': read_profile, 'user': user,
                                                             'read_qualification': read_qualification})


class DoctorDetail(DetailView):
    model = Doctor

    def get_context_data(self, **kwargs):
        context = super(DoctorDetail, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class UpdateProfile(UpdateView):
    model = Doctor
    second_model = Qualification
    form_class = ProfileForm
    # second_form_class = QualificationForm
    # fields = ['first_name', 'last_name', 'gender', 'date_of_birth', 'profession',
    #           'specialization', 'country', 'city', 'year_of_first_medical_certification', 'mobile_number',
    #           'about_me', 'hospital', 'work_number', 'avatar']

    template_name = 'userprofile/doctor_profile_update.html'

    def get_object(self, *kwargs):
        return Doctor.objects.get(user=self.request.user)

    # def get_context_data(self, **kwargs):
    #     context = super(UpdateProfile, self).get_context_data(**kwargs)
    #     pk = self.kwargs.get('pk', 0)
    #     profile_instance = self.model.objects.get(id=pk)
    #     qualification_instance = self.second_model.objects.get(doctor=profile_instance)
    #     if 'form' not in context:
    #         context['form'] = self.form_class()
    #     if 'form2' not in context:
    #         #form.instance.doctor = Doctor.objects.get(user=self.request.user)
    #         context['form2'] = self.second_form_class(instance=qualification_instance)
    #     else:
    #         context['form2'] = self.second_form_class()
    #     context['id'] = pk
    #     return context


class QualificationCreate(CreateView):
    model = Qualification
    form_class = QualificationForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        form.instance.doctor = Doctor.objects.get(user=self.request.user)
        form.instance.save()
        return super(QualificationCreate, self).form_valid(form)


class UpdateQualification(UpdateView):
    model = Qualification
    fields = ['qualification', 'university']

    template_name = 'userprofile/doctor_profile_update.html'

    def get_object(self):
        return Doctor.objects.get(user=self.request.user)


def home(request):
    return render(request, 'userprofile/home.html')


def signup(request):
    form = VerifyForm(data=request.POST)
    verified = False
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        surname = form.cleaned_data['surname']
        other_name = form.cleaned_data['other_name']
        alternative_email = form.cleaned_data['alternative_email']
        if Medic.objects.filter(email=email, surname__iexact=surname, other_name__iexact=other_name,
                                status=False).exists():
            qs = Medic.objects.get(email=email)
            generate_password = User.objects.make_random_password(8)
            user = User.objects.create_user(username=surname + other_name, email=email,
                                            password=generate_password)
            doctor = Doctor.objects.create(last_name=surname, first_name=other_name, user=user)
            current_site = get_current_site(request)
            subject = 'Welcome to 360MedNet.'
            message = render_to_string('userprofile/activate_email.html', {
                'user': user,
                'doctor': doctor,
                'domain': current_site.domain,
                'password': generate_password

            })
            to_email = [email, alternative_email]
            email = EmailMessage(subject, message, to=[to_email])
            email.send()
            # return HttpResponse('Check your email to activate your account')
            return HttpResponseRedirect(reverse('signup_activate'))

            # return HttpResponseRedirect(reverse('url_name'))
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
    fields = ['first_name', 'last_name', 'profession', 'country']

    template_name = 'userprofile/register_update.html'
    success_url = 'login'
