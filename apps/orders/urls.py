from django.urls import path
from .views import (
    OrderCreateAPIView,
    UserGroupedOrdersAPIView
)

urlpatterns = [
    path("create", OrderCreateAPIView.as_view()),
    path("by-user", UserGroupedOrdersAPIView.as_view()),
]
