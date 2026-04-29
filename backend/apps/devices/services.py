import hashlib
import logging

from django.utils import timezone

from .models import Device

logger = logging.getLogger(__name__)


def generate_device_id(user, request):
    user_agent = request.META.get("HTTP_USER_AGENT", "")
    ip = request.META.get("REMOTE_ADDR", "")

    raw = f"{user.id}-{user_agent}-{ip}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def register_device(user, request):
    device_id = generate_device_id(user, request)

    ip = request.META.get("REMOTE_ADDR", "") or ""
    user_agent = request.META.get("HTTP_USER_AGENT", "") or ""

    device, created = Device.objects.get_or_create(
        device_id=device_id,
        defaults={
            "user": user,
            "ip_address": ip,
            "user_agent": user_agent,
        },
    )

    is_new_device = created
    # Always refresh last_seen on every successful login/activation attempt.
    device.last_seen = timezone.now()
    device.save(update_fields=["last_seen"])

    if is_new_device:
        logger.info(
            "New device detected.",
            extra={"user_id": str(user.id), "device_id": device_id},
        )
    else:
        logger.info(
            "Existing device reused.",
            extra={"user_id": str(user.id), "device_id": device_id},
        )

    return device, is_new_device


def get_user_device_count(user):
    """
    Helper for multi-device intelligence signals.

    Counts active devices associated with the user.
    """
    return Device.objects.filter(user=user, is_active=True).count()

