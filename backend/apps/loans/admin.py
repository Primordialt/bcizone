from django.contrib import admin

from .models import LoanApplication


@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "amount",
        "tenor",
        "status",
        "interest",
        "total_repayment",
        "risk_score",
        "risk_level",
        "created_at",
    )
    list_filter = ("status", "risk_level", "created_at")
    search_fields = ("user__email", "status", "risk_level")

