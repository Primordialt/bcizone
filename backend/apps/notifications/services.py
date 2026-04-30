import logging

from .models import (
    Notification,
    NotificationChannel,
    NotificationEventType,
    NotificationStatus,
)
from .tasks import send_notification_task

TEMPLATES = {
    NotificationEventType.OTP: "Your OTP code is {code}",
    NotificationEventType.LOAN_APPROVED: "Your loan of {amount} has been approved",
    NotificationEventType.DISBURSEMENT_SUCCESS: "Your loan has been disbursed successfully",
    NotificationEventType.PAYMENT_RECEIVED: "We have received your payment of {amount}",
}

logger = logging.getLogger(__name__)


def send_notification(user, event_type, channel="SMS", context=None):
    context = context or {}
    template = TEMPLATES.get(event_type, "")
    message = template.format(**context) if template else ""
    unique_id = context.get("unique_id")
    if not unique_id:
        logger.error(
            "Notification creation failed: unique_id missing.",
            extra={"event_type": event_type, "channel": channel, "user_id": str(user.id)},
        )
        raise ValueError("context['unique_id'] is required for deterministic notification reference.")
    reference = f"NOTIF-{event_type}-{unique_id}"

    try:
        existing = Notification.objects.filter(reference=reference).first()
        if existing:
            logger.info(
                "Notification already exists; returning existing record.",
                extra={
                    "notification_id": str(existing.id),
                    "event_type": event_type,
                    "channel": channel,
                },
            )
            return existing

        notification = Notification.objects.create(
            user=user,
            channel=channel,
            event_type=event_type,
            message=message,
            status=NotificationStatus.PENDING,
            reference=reference,
        )
        logger.info(
            "Notification created.",
            extra={
                "notification_id": str(notification.id),
                "event_type": event_type,
                "channel": channel,
            },
        )
        send_notification_task.delay(str(notification.id))
        return notification
    except Exception:
        logger.exception(
            "Notification processing error.",
            extra={"event_type": event_type, "channel": channel, "user_id": str(user.id)},
        )
        raise


def send_otp_notification(user, code):
    return send_notification(
        user=user,
        event_type=NotificationEventType.OTP,
        channel=NotificationChannel.SMS,
        context={"code": code, "unique_id": f"{user.id}-{code}"},
    )


def send_loan_approval_notification(user, amount, loan_id=None):
    return send_notification(
        user=user,
        event_type=NotificationEventType.LOAN_APPROVED,
        channel=NotificationChannel.SMS,
        context={"amount": amount, "unique_id": loan_id or f"{user.id}-{amount}"},
    )


def send_disbursement_notification(user, disbursement_id=None):
    return send_notification(
        user=user,
        event_type=NotificationEventType.DISBURSEMENT_SUCCESS,
        channel=NotificationChannel.SMS,
        context={"unique_id": disbursement_id or f"{user.id}-general"},
    )


def send_payment_notification(user, amount, payment_reference=None):
    return send_notification(
        user=user,
        event_type=NotificationEventType.PAYMENT_RECEIVED,
        channel=NotificationChannel.SMS,
        context={"amount": amount, "unique_id": payment_reference or f"{user.id}-{amount}"},
    )


def retry_notification(notification):
    if notification.status != NotificationStatus.FAILED:
        return notification
    notification.status = NotificationStatus.PENDING
    notification.save(update_fields=["status"])
    logger.info(
        "Notification retried.",
        extra={
            "notification_id": str(notification.id),
            "event_type": notification.event_type,
            "channel": notification.channel,
        },
    )
    send_notification_task.delay(str(notification.id))
    return notification

