from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    FraudAwareTokenObtainPairSerializer,
    OTPVerifySerializer,
    SignupSerializer,
)
from .services import generate_otp, verify_otp

from apps.devices.services import register_device
from apps.kyc.services import ensure_kyc_profile
from apps.notifications.services import send_otp_notification

User = get_user_model()


class SignupView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "otp"

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        ensure_kyc_profile(user)
        try:
            code = generate_otp(user.phone_number)
        except DjangoValidationError as exc:
            return Response(
                {"detail": exc.messages[0] if exc.messages else "Rate limit exceeded"},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )
        send_otp_notification(user, code)
        response_data = {
            "message": "User created. Complete verification with OTP.",
        }
        # In production, avoid returning OTPs in responses.
        if getattr(settings, "DEBUG", False):
            response_data["otp_code"] = code

        return Response(response_data, status=status.HTTP_201_CREATED)


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data["phone_number"]
        code = serializer.validated_data["code"]

        if not verify_otp(phone_number, code):
            return Response(
                {"detail": "Invalid OTP or no matching unused code."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.filter(phone_number=phone_number).first()
        if not user:
            return Response(
                {"detail": "No user found for this phone number."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not user.is_active:
            user.is_active = True
            user.save(update_fields=["is_active"])

        # Register/update device metadata on successful activation.
        register_device(user, request)

        return Response({"message": "Account activated."})


class FraudAwareTokenObtainPairView(TokenObtainPairView):
    serializer_class = FraudAwareTokenObtainPairSerializer
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "login"
