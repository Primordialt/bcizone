from django.contrib import admin

from .models import RiskAssessment


@admin.register(RiskAssessment)
class RiskAssessmentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "score", "risk_level", "decision", "created_at")
    search_fields = ("user__email", "risk_level", "decision")
    list_filter = ("risk_level", "decision", "created_at")

