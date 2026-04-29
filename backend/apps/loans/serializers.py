from decimal import Decimal

from rest_framework import serializers

from .models import LoanApplication


class LoanApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApplication
        fields = (
            "id",
            "amount",
            "tenor",
            "status",
            "interest",
            "total_repayment",
            "risk_score",
            "risk_level",
            "created_at",
        )
        read_only_fields = (
            "id",
            "status",
            "interest",
            "total_repayment",
            "risk_score",
            "risk_level",
            "created_at",
        )


class ApplyLoanSerializer(serializers.Serializer):
    amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal("0.01"),
    )
    tenor = serializers.IntegerField(min_value=1)

