"""
End-to-end tests for GET /api/purchase-requests/.

The brief is in backend/EXERCISE.md. These tests fail until both the endpoint and the
tests themselves are written; that is deliberate.
"""
import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_list_purchase_requests(client, alice, bob, pending_request):
    response = client.get(reverse("purchase-request-list"))

    pytest.fail(
        "Not implemented. Assert what GET /api/purchase-requests/ should return "
        f"for the current user; it currently answers {response.status_code}."
    )
