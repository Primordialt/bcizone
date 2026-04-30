import uuid

from django.conf import settings
from django.db import models


class FraudStatus(models.TextChoices):
    CLEAN = "CLEAN", "CLEAN"
    REVIEW = "REVIEW", "REVIEW"
    BLOCKED = "BLOCKED", "BLOCKED"


class FraudProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="fraud_profile",
    )
    score = models.IntegerField(default=0)
    flags = models.JSONField(default=list, blank=True)
    status = models.CharField(
        max_length=10,
        choices=FraudStatus.choices,
        default=FraudStatus.CLEAN,
    )
    last_evaluated = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"FraudProfile<{self.user_id}:{self.status}>"
