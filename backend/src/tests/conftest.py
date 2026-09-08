"""
Shared fixtures for the API tests.
"""
import pytest

from purchase_requests.models import PurchaseRequest

from .factories import make_approval, make_purchase_request, make_user


@pytest.fixture
def alice(db):
    """A requester: creates purchase requests, approves nothing."""
    return make_user("alice")


@pytest.fixture
def bob(db):
    """An approver: approves other people's requests, creates none."""
    return make_user("bob")


@pytest.fixture
def pending_request(alice, bob):
    """A PENDING request raised by alice, awaiting bob's decision."""
    purchase_request = make_purchase_request(alice, status=PurchaseRequest.Status.PENDING)
    make_approval(purchase_request, bob, approved=None)
    return purchase_request
