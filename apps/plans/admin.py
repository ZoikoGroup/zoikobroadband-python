from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Plan, PlanCategory, PlanVariation


class PlanVariationInline(admin.TabularInline):
    model = PlanVariation
    extra = 1
    fields = (
        "label",
        "duration_value",
        "duration_unit",
        "price",
        "currency",
        "discount_percentage",
        "bt_plan_id",
        "is_default",
        "is_active",
        "sort_order",
    )
    ordering = ("sort_order", "price")
    show_change_link = True


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
        return format_html(
            '<span style="font-weight:600">{}</span>', count
        )


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    # ------------------------------------------------------------------ #
    # List view
    # ------------------------------------------------------------------ #
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

    # ------------------------------------------------------------------ #
    # Detail view — tabbed layout via fieldsets + inline
    # ------------------------------------------------------------------ #
    fieldsets = (
        # ── Tab 1: General ──────────────────────────────────────────────
        (
            _("General"),
            {
                "fields": (
                    "category",
                    "name",
                    "slug",
                    "description",
                    ("bt_plan_id", "bt_plan_name"),
                    ("is_active", "is_featured", "sort_order"),
                ),
                "classes": ("tab",),  # used by custom CSS below
                "description": _(
                    "Core plan settings and BrainTree integration identifiers."
                ),
            },
        ),
    )

    # Variation tab lives as an inline
    inlines = [PlanVariationInline]

    # ------------------------------------------------------------------ #
    # Custom JS/CSS for a clean tabbed experience in default admin
    # ------------------------------------------------------------------ #
    class Media:
        css = {"all": ("plans/admin/plan_tabs.css",)}
        js = ("plans/admin/plan_tabs.js",)

    # ------------------------------------------------------------------ #
    # Computed columns
    # ------------------------------------------------------------------ #
    @admin.display(description=_("Variations"))
    def variation_count(self, obj):
        count = obj.variations.filter(is_active=True).count()
        color = "#2e7d32" if count else "#c62828"
        return format_html(
            '<span style="color:{};font-weight:600">{}</span>', color, count
        )

    @admin.display(description=_("Price Range"))
    def price_range(self, obj):
        variations = obj.variations.filter(is_active=True).order_by("price")
        if not variations.exists():
            return format_html('<span style="color:#999">—</span>')
        low = variations.first()
        high = variations.last()
        if low == high:
            return format_html(
                "{} {}", low.currency, low.discounted_price
            )
        return format_html(
            "{} {} – {}",
            low.currency,
            low.discounted_price,
            high.discounted_price,
        )


@admin.register(PlanVariation)
class PlanVariationAdmin(admin.ModelAdmin):
    list_display = (
        "label",
        "plan",
        "duration_display_col",
        "price",
        "currency",
        "discount_percentage",
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
                    ("price", "currency", "discount_percentage"),
                )
            },
        ),
        (
            _("BrainTree"),
            {
                "fields": ("bt_plan_id",),
                "description": _(
                    "Leave blank to inherit BrainTree Plan ID from the parent plan."
                ),
            },
        ),
        (
            _("Status"),
            {"fields": ("is_active", "is_default", "sort_order")},
        ),
    )

    @admin.display(description=_("Duration"))
    def duration_display_col(self, obj):
        return obj.duration_display

    @admin.display(description=_("BT Plan ID"))
    def effective_bt_plan_id_col(self, obj):
        eid = obj.effective_bt_plan_id
        inherited = not obj.bt_plan_id and bool(eid)
        if inherited:
            return format_html(
                '<span title="Inherited from parent plan" style="color:#888;font-style:italic">{}</span>',
                eid,
            )
        return eid or format_html('<span style="color:#ccc">—</span>')
