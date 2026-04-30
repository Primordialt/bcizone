from decimal import Decimal

import logging
from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.risk.enums import DecisionType
from apps.risk.services import calculate_risk

from .models import LoanApplication, LoanStatus


INTEREST_RATE = Decimal("0.10")
logger = logging.getLogger(__name__)


def calculate_interest(amount):
    return amount * INTEREST_RATE


def process_loan_application(user, amount, tenor, context):
    logger.info(
        "Loan processing started.",
        extra={"user_id": str(user.id), "amount": str(amount), "tenor": tenor},
    )
    try:
        if amount > Decimal("500000"):
            logger.error(
                "Loan processing failed: amount exceeds limit.",
                extra={"user_id": str(user.id), "amount": str(amount)},
            )
            raise ValidationError("Loan amount cannot exceed 500000.")

        has_active_loan = LoanApplication.objects.filter(
            user=user,
            status__in=["PENDING", "APPROVED", "REVIEW"],
        ).exists()
        if has_active_loan:
            logger.error(
                "Loan processing failed: active loan exists.",
                extra={"user_id": str(user.id)},
            )
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
            outstanding_balance=total_repayment,
            risk_score=assessment.score,
            risk_level=assessment.risk_level,
            approved_at=approved_at,
            declined_at=declined_at,
        )
        logger.info(
            "Loan application processed.",
            extra={"loan_id": str(application.id), "status": status},
        )

        if status == LoanStatus.APPROVED:
            from apps.disbursements.services import complete_disbursement, initiate_disbursement
            from apps.disbursements.models import DisbursementStatus
            from apps.repayments.services import generate_repayment_schedule

            disbursement = initiate_disbursement(application)
            disbursement = complete_disbursement(disbursement)
            from apps.notifications.services import send_loan_approval_notification

            send_loan_approval_notification(
                application.user, application.amount, loan_id=application.id
            )
            if disbursement.status == DisbursementStatus.SUCCESS:
                generate_repayment_schedule(application)
                logger.info(
                    "Repayment schedule generated.",
                    extra={"loan_id": str(application.id)},
                )

        return application
    except Exception:
        logger.exception(
            "Loan processing error.",
            extra={"user_id": str(user.id), "amount": str(amount), "tenor": tenor},
        )
        raise

