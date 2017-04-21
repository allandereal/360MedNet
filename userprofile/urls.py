from django.conf.urls import url
from django.contrib.auth import views as auth_views
from userprofile import views as user_views

urlpatterns = [
    url(r'^accounts/login/', auth_views.login, name='login', kwargs={'redirect_authenticated_user': True}),
    url(r'^accounts/verified_registration/(?P<medic_id>[0-9]+)/$', user_views.register, name='register'),
    url(r'^accounts/unverified_registration/$', user_views.unverified_register, name='unverified_register'),
    url(r'^accounts/verify/$', user_views.verify, name='verify'),
    url(r'^accounts/profile/$', user_views.profile, name='profile'),
    url(r'^accounts/logout/$', user_views.logout, name='logout'),
]
