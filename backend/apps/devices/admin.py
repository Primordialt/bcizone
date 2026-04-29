from django.contrib import admin

from .models import Device


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "device_id", "ip_address", "is_active", "last_seen")
    search_fields = ("device_id", "ip_address")

