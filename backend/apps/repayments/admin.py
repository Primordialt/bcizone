from django.contrib import admin

from .models import Payment, RepaymentSchedule


@admin.register(RepaymentSchedule)
class RepaymentScheduleAdmin(admin.ModelAdmin):
    list_display = ("id", "loan", "due_date", "amount_due", "status")
    list_filter = ("status", "due_date")
    search_fields = ("loan__id",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "loan", "amount_paid", "payment_date", "reference")
    search_fields = ("loan__id", "reference")

