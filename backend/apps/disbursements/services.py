import logging
import random

from django.utils import timezone

from apps.loans.models import LoanStatus

from .models import Disbursement, DisbursementStatus

logger = logging.getLogger(__name__)
FAILURE_RATE = 0.2


def initiate_disbursement(loan):
    """
    Create one disbursement per loan with PENDING status.
    """
    existing = Disbursement.objects.filter(loan=loan).order_by("created_at").first()
    if existing:
        logger.info(
            "Disbursement already exists; reusing existing record.",
            extra={"loan_id": str(loan.id), "disbursement_id": str(existing.id)},
        )
        return existing

    disbursement = Disbursement.objects.create(
        loan=loan,
        amount=loan.amount,
        status=DisbursementStatus.PENDING,
        reference=f"DISB-{loan.id}",
        provider="mock",
    )
    logger.info(
        "Disbursement created.",
        extra={"loan_id": str(loan.id), "disbursement_id": str(disbursement.id)},
    )
    return disbursement


def complete_disbursement(disbursement):
    """
    Simulate provider completion with random failures.
    """
    if disbursement.status == DisbursementStatus.SUCCESS:
        return disbursement

    should_fail = random.random() < FAILURE_RATE
    if should_fail:
        disbursement.status = DisbursementStatus.FAILED
        disbursement.completed_at = timezone.now()
        disbursement.save(update_fields=["status", "completed_at"])
        # Keep loan APPROVED when transfer fails.
        logger.error(
            "Disbursement failed.",
            extra={
                "loan_id": str(disbursement.loan_id),
                "disbursement_id": str(disbursement.id),
            },
        )
        return disbursement

    disbursement.status = DisbursementStatus.SUCCESS
    disbursement.completed_at = timezone.now()
    disbursement.save(update_fields=["status", "completed_at"])

    loan = disbursement.loan
    loan.status = LoanStatus.DISBURSED
    loan.save(update_fields=["status"])
    from apps.notifications.services import send_disbursement_notification

    send_disbursement_notification(loan.user, disbursement_id=disbursement.id)
    logger.info(
        "Disbursement succeeded.",
        extra={"loan_id": str(loan.id), "disbursement_id": str(disbursement.id)},
    )
    return disbursement


def retry_disbursement(disbursement):
    """
    Retry only failed disbursements.
    """
    if disbursement.status != DisbursementStatus.FAILED:
        return disbursement

    # Move back to pending before attempting completion.
    disbursement.status = DisbursementStatus.PENDING
    disbursement.completed_at = None
    disbursement.save(update_fields=["status", "completed_at"])
    logger.info(
        "Retrying disbursement.",
        extra={
            "loan_id": str(disbursement.loan_id),
            "disbursement_id": str(disbursement.id),
        },
    )
    return complete_disbursement(disbursement)

