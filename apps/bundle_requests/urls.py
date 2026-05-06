from django.urls import path
from .views import create_bundle_request

urlpatterns = [
    path('bundle-request/', create_bundle_request),
]