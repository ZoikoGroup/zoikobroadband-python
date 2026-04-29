from django.contrib import admin
from django.utils.html  import format_html
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .models import Plan, PlanCategory, PlanVariation


class PlanVariationInline(admin.TabularInline):
    model = PlanVariation
    extra = 1
    fields = (
        "label",
        "duration_value",
        "duration_unit",
        "price",
        "sale_price",
        "bt_plan_id",
        "is_default",
        "is_active",
        "sort_order",
    )
    ordering = ("sort_order", "price")
    show_change_link = True


# =========================
# Plan Category Admin
# =========================
@admin.register(PlanCategory)
class PlanCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "sort_order", "plan_count")
    list_editable = ("is_active", "sort_order")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("sort_order", "name")

    @admin.display(description=_("Plans"))
    def plan_count(self, obj):
        count = obj.plans.count()
        return format_html('<span style="font-weight:600">{}</span>', count)


# =========================
# Plan Admin
# =========================
@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "category",
        "slug",
        "bt_plan_id",
        "variation_count",
        "price_range",
        "is_featured",
        "is_active",
        "sort_order",
    )

    list_filter = ("category", "is_active", "is_featured")
    list_editable = ("is_active", "is_featured", "sort_order")
    search_fields = ("name", "slug", "bt_plan_id", "bt_plan_name")
    ordering = ("sort_order", "name")
    prepopulated_fields = {"slug": ("name",)}

    fieldsets = (
        (
            _("General"),
            {
                "fields": (
                    "category",
                    "name",
                    "slug",
                    "description",
                    "bt_plan_id", 
                    "bt_plan_name",
                    "is_active", 
                    "is_featured",
                    "sort_order",
                ),
                "classes": ("tab",),
                "description": _(
                    "Core plan settings and  integration identifiers."
                ),
            },
        ),
    )

    inlines = [PlanVariationInline]

    class Media:
        css = {"all": ("plans/admin/plan_tabs.css",)}
        js = ("plans/admin/plan_tabs.js",)

    # -------------------------
    # SAFE computed fields
    # -------------------------

    @admin.display(description=_("Variations"))
    def variation_count(self, obj):
        count = obj.variations.filter(is_active=True).count()
        color = "#2e7d32" if count else "#c62828"
        return format_html(
            '<span style="color:{};font-weight:600">{}</span>',
            color,
            count
        )

    @admin.display(description=_("Price Range"))
    def price_range(self, obj):
        variations = obj.variations.filter(is_active=True).order_by("price")

        if not variations.exists():
            return ('<span style="color:#999">—</span>')

        low = variations.first()
        high = variations.last()

        low_price = low.final_price
        high_price = high.final_price

        if low == high:
            return f"{low_price}"

        return f"{low_price} – {high_price}"

    def clean(self):
        if self.sale_price and self.sale_price > self.price:
            raise ValidationError("Sale price cannot be greater than regular price")
# =========================
# Plan Variation Admin
# =========================
@admin.register(PlanVariation)
class PlanVariationAdmin(admin.ModelAdmin):
    list_display = (
        "label",
        "plan",
        "duration_display_col",
        "price",
        "sale_price",
        "effective_bt_plan_id_col",
        "is_default",
        "is_active",
        "sort_order",
    )

    list_filter = ("plan__category", "duration_unit", "is_active", "is_default")
    list_editable = ("is_active", "is_default", "sort_order")
    search_fields = ("label", "plan__name", "bt_plan_id")
    autocomplete_fields = ("plan",)
    ordering = ("plan", "sort_order", "price")

    fieldsets = (
        (
            _("Variation Details"),
            {
                "fields": (
                    "plan",
                    "label",
                    ("duration_value", "duration_unit"),
                    ("price",),
                )
            },
        ),
        (
            _(""),
            {
                "fields": ("bt_plan_id",),
                "description": _(
                    "Leave blank to inherit BT Plan ID from the parent plan."
                ),
            },
        ),
        (
            _("Status"),
            {"fields": ("is_active", "is_default", "sort_order")},
        ),
    )

    @admin.display(description="Final Price")
    def final_price_col(self, obj):
        if obj.sale_price:
            return format_html(
                '<span style="text-decoration:line-through;color:#999;">{}</span> <strong>{}</strong>',
                obj.price,
                obj.sale_price
            )
        return str(obj.price)
    
    @admin.display(description=_("Duration"))
    def duration_display_col(self, obj):
        return obj.duration_display or "—"

    @admin.display(description=_("BT Plan ID"))
    def effective_bt_plan_id_col(self, obj):
        eid = obj.effective_bt_plan_id

        if not eid:
            return ('<span style="color:#ccc">—</span>')

        if not obj.bt_plan_id:
            return format_html(
                '<span title="Inherited from parent plan" style="color:#888;font-style:italic">{}</span>',
                eid,
            )

        return str(eid)