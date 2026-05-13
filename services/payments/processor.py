"""
Payment processor — Stripe / UPI / wallet abstraction layer.
"""
import uuid, time
from enum import Enum
from dataclasses import dataclass
from typing import Optional


class PaymentMethod(Enum):
    CARD   = "card"
    UPI    = "upi"
    WALLET = "wallet"


class PaymentStatus(Enum):
    PENDING   = "pending"
    COMPLETED = "completed"
    FAILED    = "failed"
    REFUNDED  = "refunded"


@dataclass
class Payment:
    id: str
    trip_id: str
    rider_id: str
    amount_paise: int
    currency: str
    method: PaymentMethod
    status: PaymentStatus
    provider_ref: Optional[str] = None
    created_at: float = 0.0

    @property
    def amount_display(self) -> str:
        symbol = "₹" if self.currency == "INR" else "$"
        return f"{symbol}{self.amount_paise / 100:.2f}"


class PaymentProcessor:
    def __init__(self, stripe_client=None, upi_client=None):
        self._stripe = stripe_client
        self._upi    = upi_client
        self._store: dict = {}

    def create(self, trip_id: str, rider_id: str, amount_paise: int,
               currency: str, method: PaymentMethod) -> Payment:
        p = Payment(
            id=str(uuid.uuid4()), trip_id=trip_id, rider_id=rider_id,
            amount_paise=amount_paise, currency=currency, method=method,
            status=PaymentStatus.PENDING, created_at=time.time(),
        )
        self._store[p.id] = p
        return p

    def capture(self, payment_id: str) -> Payment:
        p = self._store[payment_id]
        if p.method == PaymentMethod.WALLET:
            p.status = PaymentStatus.COMPLETED
        elif p.method == PaymentMethod.CARD and self._stripe:
            intent = self._stripe.payment_intents.confirm(p.provider_ref)
            p.status = PaymentStatus.COMPLETED if intent.status == "succeeded" else PaymentStatus.FAILED
        elif p.method == PaymentMethod.UPI and self._upi:
            result = self._upi.verify(p.provider_ref)
            p.status = PaymentStatus.COMPLETED if result["status"] == "SUCCESS" else PaymentStatus.FAILED
        return p

    def refund(self, payment_id: str, amount_paise: Optional[int] = None) -> Payment:
        p = self._store[payment_id]
        if p.status != PaymentStatus.COMPLETED:
            raise ValueError(f"Cannot refund payment with status {p.status}")
        if self._stripe and p.method == PaymentMethod.CARD:
            self._stripe.refunds.create(
                payment_intent=p.provider_ref,
                amount=amount_paise or p.amount_paise,
                idempotency_key=f"refund_{payment_id}",
            )
        p.status = PaymentStatus.REFUNDED
        return p
