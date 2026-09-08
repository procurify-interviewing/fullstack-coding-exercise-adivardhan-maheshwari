from django.urls import path

from . import views

urlpatterns = [
    path("purchase-requests/", views.list_purchase_requests, name="purchase-request-list"),
]
