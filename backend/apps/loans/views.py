from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from apps.devices.services import get_user_device_count

from .serializers import ApplyLoanSerializer, LoanApplicationSerializer
from .services import process_loan_application


class ApplyLoanView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "loan_apply"

    def post(self, request):
        serializer = ApplyLoanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        amount = serializer.validated_data["amount"]
        tenor = serializer.validated_data["tenor"]

        is_new_device = False
        device_count = get_user_device_count(user)

        context = {
            "is_new_device": is_new_device,
            "device_count": device_count,
        }
        try:
            application = process_loan_application(user, amount, tenor, context)
        except DjangoValidationError as exc:
            message = exc.messages[0] if exc.messages else "Rate limit exceeded"
            status_code = (
                status.HTTP_429_TOO_MANY_REQUESTS
                if message in {"Rate limit exceeded", "Loan blocked due to fraud risk."}
                else status.HTTP_400_BAD_REQUEST
            )
            return Response({"detail": message}, status=status_code)

        response_data = LoanApplicationSerializer(application).data
        return Response(response_data, status=status.HTTP_201_CREATED)

