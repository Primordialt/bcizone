import logging
import random
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from .models import OTP

logger = logging.getLogger(__name__)


OTP_EXPIRY = timedelta(minutes=5)
OTP_RESEND_COOLDOWN = timedelta(seconds=60)
OTP_RATE_WINDOW = timedelta(minutes=10)
MAX_OTP_PER_WINDOW = 3


def _mask_phone_number(phone_number: str) -> str:
    # Basic PII masking for logs (keep last 4 digits).
    if not phone_number:
        return ""
    return f"{'*' * max(0, len(phone_number) - 4)}{phone_number[-4:]}"


def generate_otp(phone_number):
    """
    Generate (or reuse) a 6-digit OTP for a phone number.

    Rate limiting: do not create a new OTP more than once every 60 seconds
    per phone_number (reuses an existing unused OTP within the cooldown).
    """
    with transaction.atomic():
        now = timezone.now()
        cooldown_start = now - OTP_RESEND_COOLDOWN
        otp_window_start = now - OTP_RATE_WINDOW

        otp_requests_in_window = OTP.objects.filter(
            phone_number=phone_number,
            created_at__gte=otp_window_start,
        ).count()
        if otp_requests_in_window >= MAX_OTP_PER_WINDOW:
            logger.error(
                "OTP request rate limit exceeded.",
                extra={"phone_number": _mask_phone_number(phone_number)},
            )
            raise ValidationError("Too many OTP requests")

        existing = (
            OTP.objects.filter(
                phone_number=phone_number,
                is_used=False,
                created_at__gte=cooldown_start,
            )
            .order_by("-created_at")
            .first()
        )
        if existing:
            logger.info(
                "OTP reused due to resend cooldown.",
                extra={
                    "phone_number": _mask_phone_number(phone_number),
                    "otp_id": str(existing.id),
                },
            )
            return existing.code

        # No OTP eligible for reuse; invalidate all previous unused OTPs first.
        invalidated_count = OTP.objects.filter(
            phone_number=phone_number, is_used=False
        ).update(is_used=True)
        if invalidated_count:
            logger.info(
                "Previous OTPs invalidated before new generation.",
                extra={
                    "phone_number": _mask_phone_number(phone_number),
                    "invalidated_count": invalidated_count,
                },
            )

        code = f"{random.randint(0, 999999):06d}"
        otp = OTP.objects.create(phone_number=phone_number, code=code, is_used=False)
        logger.info(
            "OTP generated.",
            extra={"phone_number": _mask_phone_number(phone_number), "otp_id": str(otp.id)},
        )
        return code


def verify_otp(phone_number, code):
    """
    Verify the latest unused OTP for a phone number.

    Reject expired OTPs (older than 5 minutes). Expired OTPs are marked as used
    to prevent repeated verification attempts against stale codes.
    """
    now = timezone.now()
    otp = (
        OTP.objects.filter(phone_number=phone_number, is_used=False)
        .order_by("-created_at")
        .first()
    )

    if not otp:
        logger.warning(
            "OTP verification failed: no unused OTP.",
            extra={"phone_number": _mask_phone_number(phone_number)},
        )
        return False

    if otp.created_at <= (now - OTP_EXPIRY):
        OTP.objects.filter(pk=otp.pk).update(is_used=True)
        logger.warning(
            "OTP verification failed: expired OTP.",
            extra={"phone_number": _mask_phone_number(phone_number), "otp_id": str(otp.id)},
        )
        return False

    if otp.code != code:
        logger.warning(
            "OTP verification failed: code mismatch.",
            extra={"phone_number": _mask_phone_number(phone_number), "otp_id": str(otp.id)},
        )
        return False

    OTP.objects.filter(pk=otp.pk).update(is_used=True)
    logger.info(
        "OTP verification success.",
        extra={"phone_number": _mask_phone_number(phone_number), "otp_id": str(otp.id)},
    )
    return True
