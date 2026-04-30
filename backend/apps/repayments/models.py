import uuid

from django.db import models


class RepaymentStatus(models.TextChoices):
    PENDING = "PENDING", "PENDING"
    PAID = "PAID", "PAID"
    OVERDUE = "OVERDUE", "OVERDUE"


class RepaymentSchedule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    loan = models.ForeignKey(
        "loans.LoanApplication",
        on_delete=models.CASCADE,
        related_name="repayment_schedules",
    )
    due_date = models.DateField()
    amount_due = models.DecimalField(max_digits=12, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(
        max_length=10,
        choices=RepaymentStatus.choices,
        default=RepaymentStatus.PENDING,
    )

    def __str__(self):
        return f"RepaymentSchedule(loan_id={self.loan_id}, due_date={self.due_date}, status={self.status})"


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    loan = models.ForeignKey(
        "loans.LoanApplication",
        on_delete=models.CASCADE,
        related_name="payments",
    )
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"Payment(loan_id={self.loan_id}, amount_paid={self.amount_paid})"

