"""
Tiny helpers for tests. No external factory library on purpose.
"""
from decimal import Decimal

from django.contrib.auth import get_user_model

from purchase_requests.models import Approval, PurchaseRequest

User = get_user_model()


def make_user(username: str):
    return User.objects.create_user(username=username, email=f"{username}@example.com")


def make_purchase_request(requester, *, status=PurchaseRequest.Status.PENDING, amount="100.00", **kwargs):
    return PurchaseRequest.objects.create(
        requester=requester,
        title=kwargs.pop("title", "Test request"),
        status=status,
        total_amount=Decimal(amount),
        **kwargs,
    )


def make_approval(purchase_request, approver, *, approved=None):
    return Approval.objects.create(purchase_request=purchase_request, approver=approver, approved=approved)
