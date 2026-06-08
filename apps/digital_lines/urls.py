from django.urls import path

from .views import DigitalLineOrderView

urlpatterns = [
    path(
        "digital-line-order/",
        DigitalLineOrderView.as_view(),
        name="digital-line-order",
    ),
]