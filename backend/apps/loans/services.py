from decimal import Decimal

from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.risk.enums import DecisionType
from apps.risk.services import calculate_risk

from .models import LoanApplication, LoanStatus


INTEREST_RATE = Decimal("0.10")


def calculate_interest(amount):
    return amount * INTEREST_RATE


def process_loan_application(user, amount, tenor, context):
    if amount > Decimal("500000"):
        raise ValidationError("Loan amount cannot exceed 500000.")

    has_active_loan = LoanApplication.objects.filter(
        user=user,
        status__in=["PENDING", "APPROVED", "REVIEW"],
    ).exists()
    if has_active_loan:
        raise ValidationError("User already has an active loan")

    assessment = calculate_risk(user, context)

    decision_to_status = {
        DecisionType.APPROVE.value: LoanStatus.APPROVED,
        DecisionType.REVIEW.value: LoanStatus.REVIEW,
        DecisionType.DECLINE.value: LoanStatus.DECLINED,
    }
    status = decision_to_status.get(assessment.decision, LoanStatus.REVIEW)

    interest = calculate_interest(amount)
    total_repayment = amount + interest
    approved_at = timezone.now() if status == LoanStatus.APPROVED else None
    declined_at = timezone.now() if status == LoanStatus.DECLINED else None

    application = LoanApplication.objects.create(
        user=user,
        amount=amount,
        tenor=tenor,
        status=status,
        interest=interest,
        total_repayment=total_repayment,
        risk_score=assessment.score,
        risk_level=assessment.risk_level,
        approved_at=approved_at,
        declined_at=declined_at,
    )
    return application

