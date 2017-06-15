from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Post
from userprofile.models import Doctor
from .forms import PostForm
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from event.models import Event
from medicalcase.models import MedicalCase


class PostCreate(CreateView):
    model = Post
    form_class = PostForm
    success_url = '/feed/'

    def form_valid(self, form):
        form.instance.doctor = Doctor.objects.get(user=self.request.user)
        form.instance.save()
        return super(PostCreate, self).form_valid(form)


class Posts(ListView):
    model = Post
    form_class = PostForm
    success_url = '/feed/'

    def render_to_response(self, context, **response_kwargs):
        top_five_latest_medical_cases = MedicalCase.objects.order_by('-created_at')[:5]
        top_five_latest_events = Event.objects.order_by('-created_on')[:5]
        context = {'top_five_latest_medical_cases': top_five_latest_medical_cases,
                   'top_five_latest_events': top_five_latest_events}

        return self.response_class(request=self.request, template=self.get_template_names(), context=context,
                                   using=self.template_engine)



