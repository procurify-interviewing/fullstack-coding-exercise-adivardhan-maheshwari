"""
Seed a small, deterministic dataset.

  python manage.py seed_data

Users (username -> id after a fresh migrate):
  alice -> 1   raises most requests, approves nothing
  bob   -> 2   approver on many requests, raises a couple of his own
  carol -> 3   both raises requests and approves
  dave  -> 4   approver on requests bob has nothing to do with

Shape of the data, from bob's point of view:
  20 purchase requests in total
  11 visible to bob   (he raised them, or he is an approver on them)
   3 awaiting bob's decision (an Approval row for bob whose `approved` is still null)

Notes for whoever runs this:
  - Users are reused rather than recreated, so their ids stay stable across re-runs.
  - created_at is assigned in groups of three, so several requests share the exact same
    timestamp and a stable sort needs a tie-breaker.
  - A handful of requests are soft-deleted (soft_deleted set), including ones bob would
    otherwise see and one still awaiting his decision. Those are excluded from the counts
    above: a soft-deleted request is not visible to anyone.
"""

from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from purchase_requests.models import Approval, PurchaseRequest

User = get_user_model()

DRAFT = PurchaseRequest.Status.DRAFT
PENDING = PurchaseRequest.Status.PENDING
APPROVED = PurchaseRequest.Status.APPROVED
REJECTED = PurchaseRequest.Status.REJECTED

# (title, requester, status, amount, soft_deleted, [(approver, approved), ...])
#
# `approved` is None for a decision that is still outstanding, True/False once made.
# Requests are listed in insertion order, which is also id order after a fresh migrate.
SEED_REQUESTS = [
    ("Laptops for new hires", "alice", PENDING, "4250.00", False, [("bob", None)]),
    ("Office chairs", "alice", DRAFT, "890.00", False, []),
    ("Conference sponsorship", "carol", APPROVED, "7500.00", False, [("bob", True)]),
    ("SaaS renewal", "alice", PENDING, "1200.00", False, [("carol", None)]),
    (
        "Catering for offsite",
        "alice",
        PENDING,
        "640.00",
        False,
        [("bob", None), ("carol", True)],
    ),
    ("Warehouse shelving", "bob", DRAFT, "3100.00", False, []),
    ("Marketing print run", "carol", REJECTED, "980.00", False, [("bob", False)]),
    ("Lab consumables", "alice", PENDING, "455.00", True, [("bob", None)]),
    ("Monitors and docks", "carol", PENDING, "2340.00", False, [("dave", None)]),
    (
        "Security audit",
        "alice",
        PENDING,
        "12000.00",
        False,
        [("bob", True), ("carol", None)],
    ),
    ("Team offsite travel", "carol", APPROVED, "5600.00", False, [("dave", True)]),
    (
        "Cloud infrastructure",
        "alice",
        APPROVED,
        "8900.00",
        False,
        [("bob", True), ("carol", True)],
    ),
    ("Printer toner restock", "alice", REJECTED, "215.00", False, [("carol", False)]),
    ("Contractor onboarding", "bob", PENDING, "1750.00", False, [("carol", None)]),
    ("Trade show booth", "carol", PENDING, "6300.00", False, [("bob", None)]),
    ("Standing desks", "alice", APPROVED, "2875.00", False, [("bob", True)]),
    ("Legal retainer", "carol", APPROVED, "4400.00", True, [("bob", True)]),
    (
        "Recruiting software",
        "alice",
        REJECTED,
        "3300.00",
        False,
        [("bob", True), ("carol", False)],
    ),
    ("Server rack upgrade", "carol", REJECTED, "9150.00", True, [("dave", False)]),
    (
        "Employee wellness stipend",
        "alice",
        APPROVED,
        "1980.00",
        False,
        [("carol", True)],
    ),
]


class Command(BaseCommand):
    help = "Reset and seed users, purchase requests and approvals for the exercise."

    @transaction.atomic
    def handle(self, *args, **options):
        Approval.objects.all().delete()
        PurchaseRequest.objects.all().delete()

        # Seeded data: alice (id=1), bob (id=2), carol (id=3), dave (id=4)
        users = {
            name: self._get_or_create_user(name)
            for name in ("alice", "bob", "carol", "dave")
        }
        base = timezone.now().replace(microsecond=0) - timedelta(days=30)

        PurchaseRequest.objects.bulk_create(
            PurchaseRequest(
                requester=users[requester],
                title=title,
                status=status,
                total_amount=Decimal(amount),
                # Groups of three share the same created_at on purpose.
                created_at=base + timedelta(hours=i // 3),
                soft_deleted=soft_deleted,
            )
            for i, (title, requester, status, amount, soft_deleted, _) in enumerate(
                SEED_REQUESTS
            )
        )

        approvals = []
        for pr, (*_, approver_specs) in zip(
            PurchaseRequest.objects.order_by("id"), SEED_REQUESTS
        ):
            for approver, approved in approver_specs:
                approvals.append(
                    Approval(
                        purchase_request=pr,
                        approver=users[approver],
                        approved=approved,
                        decided_at=(
                            pr.created_at + timedelta(hours=2)
                            if approved is not None
                            else None
                        ),
                    )
                )
        Approval.objects.bulk_create(approvals)

        self._report(users["bob"])

    def _report(self, bob):
        live = PurchaseRequest.objects.filter(soft_deleted=False)
        visible = live.filter(Q(requester=bob) | Q(approvals__approver=bob)).distinct()
        awaiting = live.filter(
            approvals__approver=bob, approvals__approved__isnull=True
        ).distinct()

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {User.objects.count()} users, {PurchaseRequest.objects.count()} purchase requests "
                f"({PurchaseRequest.objects.filter(soft_deleted=True).count()} soft-deleted), "
                f"{Approval.objects.count()} approvals."
            )
        )
        self.stdout.write(
            f"  bob sees {visible.count()} requests, "
            f"{awaiting.count()} of them awaiting his decision."
        )
        for username in ("alice", "bob", "carol", "dave"):
            user = User.objects.get(username=username)
            self.stdout.write(f"  {user.username}: id={user.id}")

    @staticmethod
    def _get_or_create_user(username: str):
        user, _ = User.objects.get_or_create(
            username=username, defaults={"email": f"{username}@example.com"}
        )
        return user
