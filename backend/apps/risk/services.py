from .enums import DecisionType, RiskLevel
from .models import RiskAssessment
from .rules import check_account_age, check_device_count, check_new_device


def calculate_risk(user, context):
    """
    Calculate risk using rule-based score contributions.

    context:
      - is_new_device (bool)
      - device_count (int) [accepted but current rules derive from device model]
    """
    is_new_device = bool(context.get("is_new_device", False))

    new_device_score = check_new_device(user, is_new_device)
    device_count_score = check_device_count(user)
    account_age_score = check_account_age(user)

    total_score = new_device_score + device_count_score + account_age_score

    # Decision thresholds (centralized for maintainability).
    if total_score < 30:
        risk_level = RiskLevel.LOW
        decision = DecisionType.APPROVE
    elif 30 <= total_score <= 70:
        risk_level = RiskLevel.MEDIUM
        decision = DecisionType.REVIEW
    else:
        risk_level = RiskLevel.HIGH
        decision = DecisionType.DECLINE

    reason_parts = [
        f"new_device={new_device_score}",
        f"device_count={device_count_score}",
        f"account_age={account_age_score}",
        f"total_score={total_score}",
    ]

    assessment = RiskAssessment.objects.create(
        user=user,
        score=total_score,
        risk_level=risk_level.value,
        decision=decision.value,
        reason=", ".join(reason_parts),
    )

    return assessment

