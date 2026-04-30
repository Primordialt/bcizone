import logging

from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.fraud.models import FraudStatus
from apps.fraud.services import evaluate_fraud

from .models import (
    KYCProfile,
    KYCStatus,
    KYCVerification,
    VerificationStatus,
    VerificationType,
)

logger = logging.getLogger(__name__)


REQUIRED_KYC_FIELDS = ("full_name", "date_of_birth", "phone_number")


def ensure_kyc_profile(user):
    profile, _ = KYCProfile.objects.get_or_create(
        user=user,
        defaults={"status": KYCStatus.PENDING},
    )
    return profile


def create_kyc_profile(user, data):
    missing_fields = [
        field for field in REQUIRED_KYC_FIELDS if data.get(field) in (None, "")
    ]
    if missing_fields:
        raise ValidationError(
            {"missing_fields": f"Required fields missing: {', '.join(missing_fields)}"}
        )

    phone_number = data["phone_number"]
    full_name = data["full_name"]
    date_of_birth = data["date_of_birth"]

    risk_flag = str(phone_number) != str(user.phone_number)
    if risk_flag:
        logger.error(
            "KYC risk flag raised: phone mismatch.",
            extra={"user_id": str(user.id)},
        )

    # KYC submissions are pending until explicit verification.
    status = KYCStatus.PENDING

    profile, _ = KYCProfile.objects.update_or_create(
        user=user,
        defaults={
            "full_name": full_name,
            "date_of_birth": date_of_birth,
            "phone_number": phone_number,
            "bvn": data.get("bvn"),
            "nin": data.get("nin"),
            "status": status,
            "risk_flag": risk_flag,
        },
    )
    return profile


def evaluate_kyc_risk(user):
    profile = KYCProfile.objects.filter(user=user).first()
    if not profile:
        return "reject"

    if profile.status == KYCStatus.REJECTED:
        return "reject"

    identity_incomplete = not profile.full_name or not profile.date_of_birth
    phone_mismatch = str(profile.phone_number or "") != str(user.phone_number or "")
    if phone_mismatch and not profile.risk_flag:
        profile.risk_flag = True
        profile.save(update_fields=["risk_flag", "updated_at"])
        logger.error(
            "KYC risk flag raised during evaluation: phone mismatch.",
            extra={"user_id": str(user.id), "kyc_profile_id": str(profile.id)},
        )

    if profile.risk_flag or identity_incomplete or profile.status != KYCStatus.VERIFIED:
        return "review"

    return "clean"


def verify_identity(user, verification_type, identifier):
    verification_type = (verification_type or "").upper()
    identifier = (identifier or "").strip()
    fraud_profile = evaluate_fraud(user, {"verification_attempt": True})
    if fraud_profile.status == FraudStatus.BLOCKED:
        logger.error(
            "KYC verification blocked by fraud detection.",
            extra={"user_id": str(user.id), "fraud_score": fraud_profile.score},
        )
        raise ValidationError("Verification blocked due to fraud risk.")

    if verification_type not in VerificationType.values:
        raise ValidationError("verification_type must be BVN or NIN.")
    if not identifier:
        raise ValidationError("identifier is required.")

    existing_success = (
        KYCVerification.objects.filter(
            user=user,
            verification_type=verification_type,
            identifier=identifier,
            status=VerificationStatus.SUCCESS,
        )
        .order_by("-created_at")
        .first()
    )
    if existing_success:
        logger.info(
            "KYC verification skipped: already verified.",
            extra={
                "user_id": str(user.id),
                "verification_type": verification_type,
            },
        )
        return existing_success

    logger.info(
        "KYC verification started.",
        extra={
            "user_id": str(user.id),
            "verification_type": verification_type,
        },
    )
    verification = KYCVerification.objects.create(
        user=user,
        verification_type=verification_type,
        identifier=identifier,
        status=VerificationStatus.PENDING,
    )

    is_valid_length = len(identifier) == 11
    if is_valid_length:
        verification.status = VerificationStatus.SUCCESS
        verification.response_data = {
            "verified": True,
            "provider": "mock",
            "message": f"{verification_type} verified",
        }
        logger.info(
            "KYC verification succeeded.",
            extra={
                "user_id": str(user.id),
                "verification_id": str(verification.id),
                "verification_type": verification_type,
            },
        )
    else:
        verification.status = VerificationStatus.FAILED
        verification.response_data = {
            "verified": False,
            "provider": "mock",
            "message": f"Invalid {verification_type} length",
        }
        logger.error(
            "KYC verification failed.",
            extra={
                "user_id": str(user.id),
                "verification_id": str(verification.id),
                "verification_type": verification_type,
            },
        )

    verification.completed_at = timezone.now()
    verification.save(update_fields=["status", "response_data", "completed_at"])
    evaluate_fraud(
        user,
        {"failed_verification_attempt": verification.status == VerificationStatus.FAILED},
    )

    if verification.status == VerificationStatus.SUCCESS:
        profile = ensure_kyc_profile(user)
        profile.status = KYCStatus.VERIFIED
        if verification_type == VerificationType.BVN:
            profile.bvn = identifier
        elif verification_type == VerificationType.NIN:
            profile.nin = identifier
        profile.save(update_fields=["status", "bvn", "nin", "updated_at"])

    return verification
