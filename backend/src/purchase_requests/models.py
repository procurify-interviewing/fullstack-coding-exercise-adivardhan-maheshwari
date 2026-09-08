from django.conf import settings
from django.db import models
from django.utils import timezone


class PurchaseRequest(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT"
        PENDING = "PENDING"
        APPROVED = "APPROVED"
        REJECTED = "REJECTED"

    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="purchase_requests",
    )
    title = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.DRAFT
    )
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    soft_deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"PR#{self.pk} {self.title} ({self.status})"


class Approval(models.Model):
    """
    One row per (purchase request, approver).
    approved: None = pending, True = approved, False = rejected.
    """

    purchase_request = models.ForeignKey(
        PurchaseRequest, on_delete=models.CASCADE, related_name="approvals"
    )
    approver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="approvals"
    )
    approved = models.BooleanField(null=True, blank=True)
    decided_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["purchase_request", "approver"],
                name="uniq_approval_per_approver",
            )
        ]

    def __str__(self) -> str:
        return f"Approval(pr={self.purchase_request_id}, approver={self.approver_id}, approved={self.approved})"
