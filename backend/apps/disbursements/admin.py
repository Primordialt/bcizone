from django.contrib import admin

from .models import Disbursement


@admin.register(Disbursement)
class DisbursementAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "loan",
        "amount",
        "status",
        "reference",
        "provider",
        "created_at",
        "completed_at",
    )
    list_filter = ("status", "provider", "created_at")
    search_fields = ("reference", "loan__id")

