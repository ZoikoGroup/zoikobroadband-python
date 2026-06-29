from django.contrib import admin

from .models import DigitalLineOrder


# @admin.register(DigitalLineOrder)
# class DigitalLineOrderAdmin(admin.ModelAdmin):

#     list_display = (
#         "id",
#         "plan",
#         "duration",
#         "number_option",
#         "number_import",
#         "status",
#         "email_sent",
#         "created_at",
#     )

#     list_filter = (
#         "status",
#         "email_sent",
#         "created_at",
#         "plan",
#     )

#     search_fields = (
#         "plan",
#         "number_option",
#         "number_import",
#     )

#     readonly_fields = (
#         "created_at",
#     )

@admin.register(DigitalLineOrder)
class DigitalLineOrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "plan",
        "duration",
        "number_option",
        "number_sub_allocation",
        "number_import",
        "monthly_total",
        "one_off_total",
        "total_due_today",
        "status",
        "email_sent",
        "created_at",
    )

    list_filter = (
        "status",
        "email_sent",
        "plan",
        "duration",
        "created_at",
    )

    search_fields = (
        "plan",
        "duration",
        "number_option",
        "number_sub_allocation",
        "number_import",
    )

    readonly_fields = (
        "created_at",
    )