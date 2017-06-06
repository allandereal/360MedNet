from django.conf.urls import url
from invitation import views as invitation_views

urlpatterns = [
    url(r'^invite/$', invitation_views.invite_user, name='invite'),
    url(r'^join/(?P<code>[a-zA-Z0-9]+)/$', invitation_views.join, name='join'),
    url(r'^register_invitee/$', invitation_views.register_invited_user, name='register_invited_user')
]
