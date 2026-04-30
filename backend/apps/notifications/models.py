import uuid

from django.db import models


class NotificationChannel(models.TextChoices):
    SMS = "SMS", "SMS"
    EMAIL = "EMAIL", "EMAIL"


class NotificationEventType(models.TextChoices):
    OTP = "OTP", "OTP"
    LOAN_APPROVED = "LOAN_APPROVED", "LOAN_APPROVED"
    DISBURSEMENT_SUCCESS = "DISBURSEMENT_SUCCESS", "DISBURSEMENT_SUCCESS"
    PAYMENT_RECEIVED = "PAYMENT_RECEIVED", "PAYMENT_RECEIVED"


class NotificationStatus(models.TextChoices):
    PENDING = "PENDING", "PENDING"
    SENT = "SENT", "SENT"
    FAILED = "FAILED", "FAILED"


class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="notifications")

    channel = models.CharField(max_length=10, choices=NotificationChannel.choices)
    event_type = models.CharField(
        max_length=30,
        choices=NotificationEventType.choices,
        default=NotificationEventType.OTP,
    )
    message = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=NotificationStatus.choices,
        default=NotificationStatus.PENDING,
    )

    reference = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Notification(user_id={self.user_id}, channel={self.channel}, status={self.status})"

