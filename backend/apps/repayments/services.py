from decimal import Decimal, ROUND_HALF_UP
from datetime import timedelta

import logging
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import F, Sum
from django.utils import timezone

from apps.loans.models import LoanStatus

from .models import Payment, RepaymentSchedule, RepaymentStatus

logger = logging.getLogger(__name__)


def _round_money(value):
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def generate_repayment_schedule(loan):
    """
    Split loan.total_repayment into equal installments.
    Example guidance: 30 days -> 3 payments.
    """
    installments = max(1, loan.tenor // 10)
    total = _round_money(loan.total_repayment)

    base_amount = _round_money(total / installments)
    due_dates = [timezone.now().date() + timedelta(days=(idx + 1) * 10) for idx in range(installments)]

    schedules = []
    remaining = total
    for idx, due_date in enumerate(due_dates):
        amount_due = base_amount if idx < installments - 1 else remaining
        amount_due = _round_money(amount_due)
        schedules.append(
            RepaymentSchedule(
                loan=loan,
                due_date=due_date,
                amount_due=amount_due,
                amount_paid=Decimal("0.00"),
                status=RepaymentStatus.PENDING,
            )
        )
        remaining = _round_money(remaining - amount_due)

    RepaymentSchedule.objects.bulk_create(schedules)
    logger.info(
        "Repayment schedule generated.",
        extra={"loan_id": str(loan.id), "installments": installments},
    )
    return schedules


@transaction.atomic
def record_payment(loan, amount, reference=None):
    """
    Record a payment and apply it to the earliest unpaid schedule(s).
    amount_due stays immutable as originally scheduled.
    Remaining per schedule is computed as (amount_due - amount_paid).
    """
    logger.info(
        "Payment recording started.",
        extra={"loan_id": str(loan.id), "reference": reference or ""},
    )
    try:
        amount = _round_money(Decimal(amount))
        if amount <= Decimal("0.00"):
            logger.error(
                "Payment failed: amount is not positive.",
                extra={"loan_id": str(loan.id), "amount": str(amount)},
            )
            raise ValidationError("Payment amount must be greater than zero.")
        if amount > _round_money(loan.outstanding_balance):
            logger.error(
                "Payment failed: amount exceeds outstanding balance.",
                extra={
                    "loan_id": str(loan.id),
                    "amount": str(amount),
                    "outstanding_balance": str(loan.outstanding_balance),
                },
            )
            raise ValidationError("Payment exceeds outstanding balance")

        if reference:
            existing_payment = Payment.objects.filter(reference=reference).first()
            if existing_payment:
                logger.info(
                    "Duplicate payment reference detected; returning existing payment.",
                    extra={"loan_id": str(loan.id), "reference": reference},
                )
                return {
                    "payment": existing_payment,
                    "remaining_unapplied_amount": Decimal("0.00"),
                    "is_duplicate": True,
                }

        today = timezone.now().date()
        pending_items = list(
            RepaymentSchedule.objects.select_for_update()
            .filter(loan=loan, status__in=[RepaymentStatus.PENDING, RepaymentStatus.OVERDUE])
            .order_by("due_date")
        )

        if not pending_items:
            logger.error(
                "Payment failed: no unpaid schedule found.",
                extra={"loan_id": str(loan.id)},
            )
            raise ValidationError("No unpaid repayment schedule found for this loan.")

        payment = Payment.objects.create(
            loan=loan,
            amount_paid=amount,
            payment_date=timezone.now(),
            reference=reference or f"PAY-{timezone.now().strftime('%Y%m%d%H%M%S%f')}",
        )

        remaining = amount
        for item in pending_items:
            if remaining <= Decimal("0.00"):
                break

            schedule_remaining = _round_money(item.amount_due - item.amount_paid)
            if schedule_remaining <= Decimal("0.00"):
                item.status = RepaymentStatus.PAID
                item.save(update_fields=["status"])
                continue

            if remaining >= schedule_remaining:
                remaining = _round_money(remaining - schedule_remaining)
                item.amount_paid = _round_money(item.amount_paid + schedule_remaining)
            else:
                item.amount_paid = _round_money(item.amount_paid + remaining)
                remaining = Decimal("0.00")

            new_remaining = _round_money(item.amount_due - item.amount_paid)
            if new_remaining <= Decimal("0.00"):
                item.status = RepaymentStatus.PAID
            elif item.due_date < today:
                item.status = RepaymentStatus.OVERDUE
            else:
                item.status = RepaymentStatus.PENDING

            item.save(update_fields=["amount_paid", "status"])

        # Refresh overdue states for all unpaid schedules.
        RepaymentSchedule.objects.filter(
            loan=loan,
            due_date__lt=today,
            status=RepaymentStatus.PENDING,
            amount_paid__lt=models.F("amount_due"),
        ).update(status=RepaymentStatus.OVERDUE)

        outstanding_balance = RepaymentSchedule.objects.filter(loan=loan).aggregate(
            total=Sum(F("amount_due") - F("amount_paid"))
        )["total"] or Decimal("0.00")
        loan.outstanding_balance = _round_money(outstanding_balance)
        if loan.outstanding_balance == Decimal("0.00"):
            loan.status = LoanStatus.REPAID
            loan.save(update_fields=["outstanding_balance", "status"])
        else:
            loan.save(update_fields=["outstanding_balance"])

        from apps.notifications.services import send_payment_notification

        send_payment_notification(
            loan.user, payment.amount_paid, payment_reference=payment.reference
        )
        logger.info(
            "Payment recorded successfully.",
            extra={
                "loan_id": str(loan.id),
                "payment_id": str(payment.id),
                "reference": payment.reference,
                "remaining_unapplied_amount": str(remaining),
            },
        )

        return {
            "payment": payment,
            "remaining_unapplied_amount": remaining,
            "is_duplicate": False,
        }
    except Exception:
        logger.exception(
            "Payment recording error.",
            extra={"loan_id": str(loan.id), "reference": reference or ""},
        )
        raise

