from django.conf.urls import url
from post import views as post_views

urlpatterns = [
    url(r'^post/$', post_views.PostCreate.as_view(), name='Post'),
    url(r'^feed/$', post_views.Posts.as_view(), name='posts')
]
