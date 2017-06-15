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



