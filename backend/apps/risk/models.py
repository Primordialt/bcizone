import uuid

from django.db import models


class RiskAssessment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="risk_assessments")

    score = models.IntegerField()
    risk_level = models.CharField(max_length=10)
    decision = models.CharField(max_length=10)
    reason = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"RiskAssessment(user_id={self.user_id}, level={self.risk_level}, decision={self.decision})"

