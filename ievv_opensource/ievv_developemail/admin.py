from django.contrib import admin

from ievv_opensource.ievv_developemail.models import DevelopEmail


@admin.register(DevelopEmail)
class DevelopEmail(admin.ModelAdmin):
    list_display = [
        'id',
        'created_datetime',
    ]

    search_fields = [
        'id',
        'raw_message',
    ]

    list_filter = [
        'created_datetime',
    ]
