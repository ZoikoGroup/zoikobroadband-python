from django.db import models


class DigitalLineOrder(models.Model):

    STATUS_CHOICES = (
        ("new", "New"),
        ("processing", "Processing"),
        ("completed", "Completed"),
    )

    created_at = models.DateTimeField(auto_now_add=True)

    # Plan
    plan = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)

    # Numbers & Porting
    number_option = models.CharField(max_length=100, blank=True, null=True)
    number_sub_allocation = models.CharField(max_length=100, blank=True, null=True)
    number_import = models.CharField(max_length=100, blank=True, null=True)

    # Multi-select
    equipment = models.JSONField(default=list, blank=True)
    addons = models.JSONField(default=list, blank=True)
    charge_changes = models.JSONField(default=list, blank=True)

    # Email Tracking
    email_sent = models.BooleanField(default=False)

    # Order Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new"
    )

    plan_summary = models.JSONField(default=dict, blank=True)

    equipment_summary = models.JSONField(default=list, blank=True)

    addons_summary = models.JSONField(default=list, blank=True)

    charge_changes_summary = models.JSONField(default=list, blank=True)

    monthly_total = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    default=0,
    )

    one_off_total = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    default=0,
    )

    total_due_today = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    default=0,
    )

    def __str__(self):
        return f"Digital Line Order #{self.id}"