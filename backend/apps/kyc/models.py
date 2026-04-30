import uuid

from django.conf import settings
from django.db import models


class KYCStatus(models.TextChoices):
    PENDING = "PENDING", "PENDING"
    VERIFIED = "VERIFIED", "VERIFIED"
    REJECTED = "REJECTED", "REJECTED"


class VerificationType(models.TextChoices):
    BVN = "BVN", "BVN"
    NIN = "NIN", "NIN"


class VerificationStatus(models.TextChoices):
    PENDING = "PENDING", "PENDING"
    SUCCESS = "SUCCESS", "SUCCESS"
    FAILED = "FAILED", "FAILED"


class KYCProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="kyc_profile",
    )

    full_name = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)

    bvn = models.CharField(max_length=20, null=True, blank=True)
    nin = models.CharField(max_length=20, null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=KYCStatus.choices,
        default=KYCStatus.PENDING,
    )
    risk_flag = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"KYCProfile<{self.user_id}>"


class KYCVerification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="kyc_verifications",
    )
    verification_type = models.CharField(
        max_length=10,
        choices=VerificationType.choices,
    )
    identifier = models.CharField(max_length=50)
    status = models.CharField(
        max_length=10,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING,
    )
    response_data = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "verification_type", "identifier"]),
        ]

    def __str__(self):
        return f"KYCVerification<{self.user_id}:{self.verification_type}>"
