from django.urls import path
from .views import BusinessBroadbandInquiryView

urlpatterns = [
    path(
        'business-inquiry/',
        BusinessBroadbandInquiryView.as_view(),
        name='business-inquiry'
    ),
]