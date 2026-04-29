from django.db.models import TextChoices


class RiskLevel(TextChoices):
    LOW = "LOW", "LOW"
    MEDIUM = "MEDIUM", "MEDIUM"
    HIGH = "HIGH", "HIGH"


class DecisionType(TextChoices):
    APPROVE = "APPROVE", "APPROVE"
    REVIEW = "REVIEW", "REVIEW"
    DECLINE = "DECLINE", "DECLINE"

