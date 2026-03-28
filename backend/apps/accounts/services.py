import random

from .models import OTP


def generate_otp(phone_number):
    code = f"{random.randint(0, 999999):06d}"
    OTP.objects.create(phone_number=phone_number, code=code)
    return code


def verify_otp(phone_number, code):
    otp = (
        OTP.objects.filter(phone_number=phone_number, is_used=False)
        .order_by("-created_at")
        .first()
    )
    if not otp or otp.code != code:
        return False
    otp.is_used = True
    otp.save(update_fields=["is_used"])
    return True
