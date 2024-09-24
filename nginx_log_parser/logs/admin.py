from django.contrib import admin
from .models import LogEntry

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'date', 'http_method', 'uri', 'response_code', 'response_size')
    list_filter = ('http_method', 'response_code')
    search_fields = ('ip_address', 'uri')



