from django.contrib import admin
from .models import Order
from django.utils.safestring  import mark_safe
import json


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at")
    ordering = ("-created_at",)
    readonly_fields = ("formatted_json",)

    fieldsets = (
        (" Order Payload", {
            "classes": ("collapse",),
            "fields": ("formatted_json",),
        }),
    )

    def formatted_json(self, obj):
        pretty = json.dumps(obj.raw_data, indent=4, sort_keys=True)

        return mark_safe(
            """
            <div style="
                background:#0f172a;
                color:#e5e7eb;
                padding:15px;
                border-radius:10px;
                font-family: monospace;
                font-size:13px;
                max-height:600px;
                overflow:auto;
                white-space:pre;
            ">{}</div>
            """,
            pretty
        )

    formatted_json.short_description = " JSON Data"
