from django.conf.urls import url
from django.contrib.auth import views as auth_views
from userprofile import views as user_views

urlpatterns = [
    url(r'^login/', auth_views.login, name='login',  kwargs={'redirect_authenticated_user': True,
                                                             'template_name': 'userprofile/login.html'}),
    url(r'^accounts/verified_registration/(?P<medic_id>[0-9]+)$', user_views.register, name='register'),
    url(r'^accounts/unverified_registration/$', user_views.unverified_register, name='unverified_register'),
    url(r'^$', user_views.verify, name='verify'),
    url(r'^accounts/profile/(?P<username>[a-zA-Z0-9]+)$', user_views.get_profile, name='profile'),
    url(r'^accounts/update/(?P<pk>[\-\w]+)/$', user_views.UpdateProfile.as_view(), name='update_doctor'),
    url(r'^logout/$', user_views.logout, name='logout'),
]
