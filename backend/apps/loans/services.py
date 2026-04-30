from decimal import Decimal

import logging
from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.fraud.models import FraudStatus
from apps.fraud.services import evaluate_fraud
from apps.kyc.models import KYCProfile, KYCStatus
from apps.kyc.services import evaluate_kyc_risk
from apps.risk.enums import DecisionType
from apps.risk.services import calculate_risk

from .models import LoanApplication, LoanStatus


INTEREST_RATE = Decimal("0.10")
MAX_DAILY_LOAN_APPLICATIONS = 3
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

        today = timezone.now().date()
        daily_loan_requests = LoanApplication.objects.filter(
            user=user,
            created_at__date=today,
        ).count()
        if daily_loan_requests >= MAX_DAILY_LOAN_APPLICATIONS:
            logger.error(
                "Loan request daily rate limit exceeded.",
                extra={"user_id": str(user.id)},
            )
            raise ValidationError("Rate limit exceeded")

        kyc_profile = KYCProfile.objects.filter(user=user).first()
        if not kyc_profile:
            logger.error(
                "Loan blocked: missing KYC profile.",
                extra={"user_id": str(user.id)},
            )
            raise ValidationError("KYC required")
        kyc_evaluation = evaluate_kyc_risk(user)
        if kyc_evaluation == "reject":
            logger.error(
                "Loan blocked: KYC evaluation rejected.",
                extra={"user_id": str(user.id), "kyc_profile_id": str(kyc_profile.id)},
            )
            raise ValidationError("KYC required")
        if kyc_profile.risk_flag:
            logger.error(
                "KYC flags risk for loan processing.",
                extra={"user_id": str(user.id), "kyc_profile_id": str(kyc_profile.id)},
            )

        fraud_profile = evaluate_fraud(user, context)
        if fraud_profile.status == FraudStatus.BLOCKED:
            logger.error(
                "Loan blocked by fraud detection.",
                extra={"user_id": str(user.id), "fraud_score": fraud_profile.score},
            )
            raise ValidationError("Loan blocked due to fraud risk.")

        assessment = calculate_risk(user, context)

        decision_to_status = {
            DecisionType.APPROVE.value: LoanStatus.APPROVED,
            DecisionType.REVIEW.value: LoanStatus.REVIEW,
            DecisionType.DECLINE.value: LoanStatus.DECLINED,
        }
        status = decision_to_status.get(assessment.decision, LoanStatus.REVIEW)
        if kyc_profile.status != KYCStatus.VERIFIED:
            logger.info(
                "KYC blocks auto-approval; loan moved to REVIEW.",
                extra={
                    "user_id": str(user.id),
                    "kyc_profile_id": str(kyc_profile.id),
                    "kyc_status": kyc_profile.status,
                },
            )
            status = LoanStatus.REVIEW
        if fraud_profile.status == FraudStatus.REVIEW:
            logger.info(
                "Fraud review required; loan moved to REVIEW.",
                extra={"user_id": str(user.id), "fraud_score": fraud_profile.score},
            )
            status = LoanStatus.REVIEW

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

