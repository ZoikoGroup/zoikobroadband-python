from django.contrib import admin

from .models import (
    FaultReport,
    FaultStatusHistory,
)


class FaultStatusHistoryInline(admin.TabularInline):
    model = FaultStatusHistory
    extra = 0
    readonly_fields = (
        "status",
        "note",
        "created_at",
        "updated_by",
    )


@admin.register(FaultReport)
class FaultReportAdmin(admin.ModelAdmin):

    list_display = (
        "reference_number",
        "full_name",
        "issue_type",
        "priority",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "priority",
        "issue_type",
    )

    search_fields = (
        "reference_number",
        "full_name",
        "email",
        "phone",
    )

    readonly_fields = (
        "reference_number",
        "created_at",
        "updated_at",
    )

    inlines = [
        FaultStatusHistoryInline
    ]