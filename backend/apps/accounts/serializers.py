from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


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
