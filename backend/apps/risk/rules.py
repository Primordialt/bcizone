from datetime import timedelta

from django.utils import timezone

# Keep rule weights centralized so they are easy to adjust.
SCORE_WEIGHTS = {
    "new_device": 20,
    "device_count_low": 10,
    "device_count_medium": 25,
    "device_count_high": 40,
    "account_age_under_7_days": 35,
    "account_age_under_30_days": 15,
}

DEVICE_COUNT_THRESHOLDS = {
    "low": 1,      # count <= low
    "medium": 3,   # count <= medium
}

ACCOUNT_AGE_THRESHOLDS = {
    "under_7_days": timedelta(days=7),
    "under_30_days": timedelta(days=30),
}


def check_new_device(user, is_new_device):
    # New devices increase risk.
    return SCORE_WEIGHTS["new_device"] if is_new_device else 0


def check_device_count(user):
    # Risk increases with number of active devices.
    # Import here to avoid circular imports at module load time.
    device_qs = getattr(user, "devices", None)
    if device_qs is None:
        return 0

    active_count = device_qs.filter(is_active=True).count()

    if active_count <= DEVICE_COUNT_THRESHOLDS["low"]:
        return SCORE_WEIGHTS["device_count_low"]
    if active_count <= DEVICE_COUNT_THRESHOLDS["medium"]:
        return SCORE_WEIGHTS["device_count_medium"]
    return SCORE_WEIGHTS["device_count_high"]


def check_account_age(user):
    # Risk decreases as account ages.
    if not getattr(user, "created_at", None):
        return 0

    age = timezone.now() - user.created_at
    if age < ACCOUNT_AGE_THRESHOLDS["under_7_days"]:
        return SCORE_WEIGHTS["account_age_under_7_days"]
    if age < ACCOUNT_AGE_THRESHOLDS["under_30_days"]:
        return SCORE_WEIGHTS["account_age_under_30_days"]
    return 0

