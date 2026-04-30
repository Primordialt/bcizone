import logging

from django.utils import timezone

from apps.devices.services import get_user_device_count
from apps.kyc.models import KYCProfile, KYCVerification, VerificationStatus

from .models import FraudProfile, FraudStatus

logger = logging.getLogger(__name__)

NEW_DEVICE_SCORE = 20
MANY_DEVICES_SCORE = 30
KYC_MISMATCH_SCORE = 40
FAILED_VERIFICATION_SCORE = 50


def evaluate_fraud(user, context=None):
    context = context or {}
    score = 0
    flags = []

    is_new_device = bool(context.get("is_new_device", False))
    if is_new_device:
        score += NEW_DEVICE_SCORE
        flags.append("new_device_login")

    device_count = get_user_device_count(user)
    if device_count > 3:
        score += MANY_DEVICES_SCORE
        flags.append("multiple_devices")

    kyc_profile = KYCProfile.objects.filter(user=user).first()
    if kyc_profile and kyc_profile.risk_flag:
        score += KYC_MISMATCH_SCORE
        flags.append("kyc_mismatch")

    failed_verification_attempts = KYCVerification.objects.filter(
        user=user,
        status=VerificationStatus.FAILED,
    ).count()
    if failed_verification_attempts > 0:
        score += FAILED_VERIFICATION_SCORE
        flags.append("failed_verification_attempts")

    if score < 40:
        status = FraudStatus.CLEAN
    elif 40 <= score <= 80:
        status = FraudStatus.REVIEW
    else:
        status = FraudStatus.BLOCKED

    profile, _ = FraudProfile.objects.update_or_create(
        user=user,
        defaults={
            "score": score,
            "flags": flags,
            "status": status,
            "last_evaluated": timezone.now(),
        },
    )
    logger.info(
        "Fraud evaluation completed.",
        extra={
            "user_id": str(user.id),
            "fraud_status": status,
            "fraud_score": score,
            "failed_verification_attempts": failed_verification_attempts,
        },
    )
    return profile
