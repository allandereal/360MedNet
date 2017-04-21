from django.contrib import admin
from .models import Record, Medic, Doctor


class RecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'synced', 'created_on')
    list_filter = ['created_on']
    search_fields = ['file']


admin.site.register(Record, RecordAdmin)
admin.site.register(Medic)
admin.site.register(Doctor)
