
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from organizations.backends import invitation_backend

urlpatterns = [
    url(r'^invitations/', include('invitations.urls', namespace='invitations')),
    url(r'^accounts/', include('organizations.urls')),
    url(r'^invitations/', include(invitation_backend().get_urls())),
    url(r'^friendship/', include('friendship.urls')),
    url(r'^\.well-known/', include('letsencrypt.urls')),
    url(r'^', include('medicalcase.urls')),
    url(r'^', include('post.urls')),
    url(r'^', include('userprofile.urls')),
    url(r'^', include('website.urls')),
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    url(r'^mednet/admins/', admin.site.urls),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
