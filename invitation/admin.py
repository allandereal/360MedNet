from django.contrib import admin
from .models import Invitation, FriendInvitation


class InvitationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'organization', 'email', 'code', 'accepted', 'created_on', 'updated_on')
    list_filter = ['created_on']
    search_fields = ['name', 'email', 'organization']


class FriendInvitationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'code', 'accepted', 'sender', 'created_on', 'updated_on')
    list_filter = ['created_on']
    search_fields = ['name', 'email', 'sender']


admin.site.register(Invitation, InvitationAdmin)
admin.site.register(FriendInvitation, FriendInvitationAdmin)
