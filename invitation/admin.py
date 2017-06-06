from django.contrib import admin
from .models import Invitation


class InvitationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'organization', 'email', 'code', 'accepted')
    list_filter = ['created_on']
    search_fields = ['name', 'email', 'organization']


admin.site.register(Invitation, InvitationAdmin)
