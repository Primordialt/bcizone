import logging

from apps.kyc.models import KYCProfile

from .enums import DecisionType, RiskLevel
from .models import RiskAssessment
from .rules import check_account_age, check_device_count, check_new_device

logger = logging.getLogger(__name__)
KYC_RISK_SCORE_BONUS = 25


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
    kyc_profile = KYCProfile.objects.filter(user=user).first()
    kyc_risk_applied = bool(kyc_profile and kyc_profile.risk_flag)
    if kyc_risk_applied:
        total_score += KYC_RISK_SCORE_BONUS
        logger.error(
            "KYC flagged risk during risk assessment.",
            extra={"user_id": str(user.id), "kyc_profile_id": str(kyc_profile.id)},
        )

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

    if kyc_risk_applied:
        decision = DecisionType.REVIEW
        risk_level = RiskLevel.MEDIUM if total_score <= 70 else RiskLevel.HIGH

    reason_parts = [
        f"new_device={new_device_score}",
        f"device_count={device_count_score}",
        f"account_age={account_age_score}",
        f"kyc_risk_bonus={KYC_RISK_SCORE_BONUS if kyc_risk_applied else 0}",
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

