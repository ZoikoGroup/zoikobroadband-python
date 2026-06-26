from django.urls import path

from .views import (
    FaultReportView,
    MyFaultsView,
    FaultDetailView,
)

urlpatterns = [

    path(
        "report/",
        FaultReportView.as_view(),
        name="fault-report",
    ),

    path(
        "my-faults/",
        MyFaultsView.as_view(),
        name="my-faults",
    ),

    path(
        "<uuid:id>/",
        FaultDetailView.as_view(),
        name="fault-detail",
    ),
]