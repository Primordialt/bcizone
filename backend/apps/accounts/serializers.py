import logging

from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings as jwt_api_settings

from apps.devices.services import register_device
from apps.fraud.models import FraudStatus
from apps.fraud.services import evaluate_fraud

User = get_user_model()
logger = logging.getLogger(__name__)
MAX_FAILED_LOGIN_ATTEMPTS = 5
FAILED_LOGIN_BLOCK_SECONDS = 900


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "phone_number", "password")

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data["email"],
            phone_number=validated_data["phone_number"],
            password=validated_data["password"],
            is_active=False,
        )


class OTPVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    code = serializers.CharField(max_length=6)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = User.objects.normalize_email((attrs.get("email") or "").strip())
        password = attrs.get("password", "")

        login_key = f"failed_login_attempts:{email}"
        blocked_key = f"blocked_login:{email}"
        if cache.get(blocked_key):
            raise serializers.ValidationError("Too many attempts")

        # normalize_email only lowercases the domain; local-part case can differ from signup.
        user = User.objects.filter(email__iexact=email).first()
        if user is None:
            attempts = cache.get(login_key, 0) + 1
            cache.set(login_key, attempts, FAILED_LOGIN_BLOCK_SECONDS)
            if attempts > MAX_FAILED_LOGIN_ATTEMPTS:
                cache.set(blocked_key, True, FAILED_LOGIN_BLOCK_SECONDS)
                raise serializers.ValidationError("Too many attempts")
            raise serializers.ValidationError("Invalid credentials")

        if not user.check_password(password):
            attempts = cache.get(login_key, 0) + 1
            cache.set(login_key, attempts, FAILED_LOGIN_BLOCK_SECONDS)
            if attempts > MAX_FAILED_LOGIN_ATTEMPTS:
                cache.set(blocked_key, True, FAILED_LOGIN_BLOCK_SECONDS)
                raise serializers.ValidationError("Too many attempts")
            raise serializers.ValidationError("Invalid credentials")

        if not user.is_active:
            raise serializers.ValidationError(
                "This account is not active yet. Complete phone (OTP) verification first."
            )

        cache.delete(login_key)
        cache.delete(blocked_key)
        request = self.context.get("request")

        self.user = user
        refresh = self.get_token(user)
        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        if jwt_api_settings.UPDATE_LAST_LOGIN:
            jwt_api_settings.ON_LOGIN_SUCCESS(self.user, request)

        fraud_context = {}
        if request is not None:
            _, is_new_device = register_device(user, request)
            fraud_context["is_new_device"] = is_new_device

        fraud_profile = evaluate_fraud(user, fraud_context)
        # Staff/superuser accounts are for operations; do not lock them out of the API.
        if (
            fraud_profile.status == FraudStatus.BLOCKED
            and not user.is_superuser
            and not user.is_staff
        ):
            raise serializers.ValidationError("Account blocked due to fraud risk.")

        data["fraud_status"] = str(fraud_profile.status)
        return data
