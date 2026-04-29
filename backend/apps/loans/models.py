import uuid

from django.db import models


class LoanStatus(models.TextChoices):
    PENDING = "PENDING", "PENDING"
    APPROVED = "APPROVED", "APPROVED"
    DECLINED = "DECLINED", "DECLINED"
    REVIEW = "REVIEW", "REVIEW"


class LoanApplication(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="loan_applications")

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    tenor = models.IntegerField(help_text="Loan tenor in days")

    status = models.CharField(max_length=20, choices=LoanStatus.choices, default=LoanStatus.PENDING)

    interest = models.DecimalField(max_digits=12, decimal_places=2)
    total_repayment = models.DecimalField(max_digits=12, decimal_places=2)

    risk_score = models.IntegerField()
    risk_level = models.CharField(max_length=10)

    approved_at = models.DateTimeField(null=True, blank=True)
    declined_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"LoanApplication(user_id={self.user_id}, amount={self.amount}, status={self.status})"

