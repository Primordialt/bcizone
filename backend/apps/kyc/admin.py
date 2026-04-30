from django.contrib import admin

from .models import KYCProfile, KYCVerification


@admin.register(KYCProfile)
class KYCProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "phone_number", "status", "risk_flag", "created_at")
    list_filter = ("status", "risk_flag", "created_at")
    search_fields = ("user__email", "user__phone_number", "full_name", "phone_number", "bvn", "nin")


@admin.register(KYCVerification)
class KYCVerificationAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "verification_type",
        "identifier",
        "status",
        "created_at",
        "completed_at",
    )
    list_filter = ("verification_type", "status", "created_at")
    search_fields = ("user__email", "user__phone_number", "identifier")
