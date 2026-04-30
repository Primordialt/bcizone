from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.devices.services import register_device
from apps.fraud.models import FraudStatus
from apps.fraud.services import evaluate_fraud

User = get_user_model()
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


class FraudAwareTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username_value = attrs.get(self.username_field, "")
        login_key = f"failed_login_attempts:{username_value}"
        blocked_key = f"blocked_login:{username_value}"
        if cache.get(blocked_key):
            raise serializers.ValidationError("Too many attempts")

        try:
            data = super().validate(attrs)
        except AuthenticationFailed:
            attempts = cache.get(login_key, 0) + 1
            cache.set(login_key, attempts, FAILED_LOGIN_BLOCK_SECONDS)
            if attempts > MAX_FAILED_LOGIN_ATTEMPTS:
                cache.set(blocked_key, True, FAILED_LOGIN_BLOCK_SECONDS)
                raise serializers.ValidationError("Too many attempts")
            raise

        cache.delete(login_key)
        cache.delete(blocked_key)
        request = self.context.get("request")
        user = self.user

        fraud_context = {}
        if request is not None:
            _, is_new_device = register_device(user, request)
            fraud_context["is_new_device"] = is_new_device

        fraud_profile = evaluate_fraud(user, fraud_context)
        if fraud_profile.status == FraudStatus.BLOCKED:
            raise serializers.ValidationError("Account blocked due to fraud risk.")

        data["fraud_status"] = fraud_profile.status
        return data
