import uuid

from django.db import models


class Device(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey("accounts.User", related_name="devices", on_delete=models.CASCADE)

    # Stable fingerprint for a (user, ip, user_agent) combination.
    device_id = models.CharField(max_length=64, unique=True, db_index=True)

    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Device({self.device_id})"

