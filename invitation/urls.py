from django.conf.urls import url
from invitation import views as invitation_views

urlpatterns = [
    url(r'^invite/$', invitation_views.invite_user, name='invite'),
    url(r'^friend/invite/$', invitation_views.invite_friend, name='friend_invite'),
    url(r'^join/(?P<code>[a-zA-Z0-9]+)/$', invitation_views.join, name='join'),
    url(r'^join/friend/(?P<code>[a-zA-Z0-9]+)/$', invitation_views.join_friend_invite, name='join_friend_invite'),
    url(r'^register_medic/$', invitation_views.register_invited_user, name='register_invited_user')
]
