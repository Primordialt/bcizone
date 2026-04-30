import logging
import random

from celery import shared_task
from django.utils import timezone

from .models import Notification, NotificationChannel, NotificationStatus

logger = logging.getLogger(__name__)
FAILURE_RATE = 0.15


def _simulate_sms_send():
    return random.random() >= FAILURE_RATE


def _simulate_email_send():
    return random.random() >= FAILURE_RATE


def _deliver(channel):
    if channel == NotificationChannel.SMS:
        return _simulate_sms_send()
    if channel == NotificationChannel.EMAIL:
        return _simulate_email_send()
    return False


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 3})
def send_notification_task(self, notification_id):
    notification = Notification.objects.filter(id=notification_id).first()
    if not notification:
        return None

    if notification.status == NotificationStatus.SENT:
        return str(notification.id)

    if _deliver(notification.channel):
        notification.status = NotificationStatus.SENT
        notification.sent_at = timezone.now()
        notification.save(update_fields=["status", "sent_at"])
        logger.info(
            "Notification sent.",
            extra={
                "notification_id": str(notification.id),
                "event_type": notification.event_type,
                "channel": notification.channel,
            },
        )
    else:
        notification.status = NotificationStatus.FAILED
        notification.save(update_fields=["status"])
        logger.error(
            "Notification failed.",
            extra={
                "notification_id": str(notification.id),
                "event_type": notification.event_type,
                "channel": notification.channel,
            },
        )

    return str(notification.id)

