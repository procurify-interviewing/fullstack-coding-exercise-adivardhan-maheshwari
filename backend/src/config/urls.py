from django.urls import include, path

urlpatterns = [
    path("api/", include("purchase_requests.urls")),
]
