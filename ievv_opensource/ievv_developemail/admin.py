from django.contrib import admin

from ievv_opensource.ievv_developemail.models import DevelopEmail


@admin.register(DevelopEmail)
class DevelopEmailAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'subject',
        'from_email',
        'recipients',
        'created_datetime',
    ]

    search_fields = [
        'id',
        'from_email',
        'recipients',
        'raw_message',
    ]

    list_filter = [
        'created_datetime',
        'from_email',
    ]
