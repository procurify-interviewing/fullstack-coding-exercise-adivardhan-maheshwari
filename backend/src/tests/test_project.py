"""
Sanity checks that the project is wired up. 
"""
import pytest
from django.urls import reverse

from .factories import make_approval, make_purchase_request, make_user


class ProjectTests:
    @pytest.mark.django_db
    def test_endpoint_is_wired(self, client):
        response = client.get(reverse("purchase-request-list"))
        # The stub answers 501 until the endpoint is implemented.
        assert response.status_code in (200, 501)

    @pytest.mark.django_db
    def test_factories_work(self):
        alice = make_user("alice")
        bob = make_user("bob")
        purchase_request = make_purchase_request(alice)
        make_approval(purchase_request, bob)
        assert purchase_request.approvals.count() == 1
