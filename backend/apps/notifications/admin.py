from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "channel",
        "event_type",
        "status",
        "reference",
        "created_at",
        "sent_at",
    )
    list_filter = ("channel", "event_type", "status", "created_at")
    search_fields = ("reference", "user__email", "user__phone_number")

