from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import OTPVerifySerializer, SignupSerializer
from .services import generate_otp, verify_otp

User = get_user_model()


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        code = generate_otp(user.phone_number)
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

        updated = User.objects.filter(phone_number=phone_number).update(is_active=True)
        if not updated:
            return Response(
                {"detail": "No user found for this phone number."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response({"message": "Account activated."})
