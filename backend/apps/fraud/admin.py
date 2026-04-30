from django.contrib import admin

from .models import FraudProfile


@admin.register(FraudProfile)
class FraudProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "score", "status", "last_evaluated", "created_at")
    list_filter = ("status", "last_evaluated", "created_at")
    search_fields = ("user__email", "user__phone_number")
