from django.conf.urls import url
from website import views as website_views

urlpatterns = [
    url(r'^about us/$', website_views.about_us, name='about_us'),
    url(r'^privacy policy/$', website_views.privacy_policy, name='privacy_policy'),
    url(r'^terms/$', website_views.terms_of_use, name='terms_of_use'),
]
