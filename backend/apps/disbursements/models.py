import uuid

from django.db import models


class DisbursementStatus(models.TextChoices):
    PENDING = "PENDING", "PENDING"
    SUCCESS = "SUCCESS", "SUCCESS"
    FAILED = "FAILED", "FAILED"


class Disbursement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    loan = models.ForeignKey(
        "loans.LoanApplication",
        on_delete=models.CASCADE,
        related_name="disbursements",
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(
        max_length=10,
        choices=DisbursementStatus.choices,
        default=DisbursementStatus.PENDING,
    )

    reference = models.CharField(max_length=100, unique=True)
    provider = models.CharField(max_length=50, default="mock")

    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Disbursement(loan_id={self.loan_id}, amount={self.amount}, status={self.status})"

