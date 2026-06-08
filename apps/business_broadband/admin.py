from django.contrib import admin
from .models import BusinessBroadbandInquiry


@admin.register(BusinessBroadbandInquiry)
class BusinessBroadbandInquiryAdmin(admin.ModelAdmin):

    list_display = (
        'business_name',
        'contact_name',
        'email',
        'phone_number',
        'business_size',
        'email_sent',
        'created_at'
    )

    search_fields = (
        'business_name',
        'email',
        'phone_number'
    )

    list_filter = (
        'business_size',
        'email_sent',
        'created_at'
    )