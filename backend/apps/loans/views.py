from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.devices.services import get_user_device_count

from .serializers import ApplyLoanSerializer, LoanApplicationSerializer
from .services import process_loan_application


class ApplyLoanView(APIView):
    permission_classes = [IsAuthenticated]

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
        application = process_loan_application(user, amount, tenor, context)

        response_data = LoanApplicationSerializer(application).data
        return Response(response_data, status=status.HTTP_201_CREATED)

