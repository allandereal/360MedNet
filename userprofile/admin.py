from django.contrib import admin
from .models import Record, Medic, Doctor


class RecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'synced', 'created_on')
    list_filter = ['created_on']
    search_fields = ['file']

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'profession')
    list_filter = ['created_at']
    search_fields = ['first_name', 'last_name']

admin.site.register(Record, RecordAdmin)
admin.site.register(Medic)
admin.site.register(Doctor, DoctorAdmin)
