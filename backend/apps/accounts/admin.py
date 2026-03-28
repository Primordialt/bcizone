
from django.contrib import admin
from .models import User, OTP


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "phone_number", "is_active", "created_at")
    search_fields = ("email", "phone_number")


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "code", "is_used", "created_at")
    search_fields = ("phone_number",)