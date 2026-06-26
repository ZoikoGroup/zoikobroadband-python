from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid

User = get_user_model()


class FaultReport(models.Model):

    STATUS_CHOICES = [
        ("submitted", "Submitted"),
        ("assigned", "Engineer Assigned"),
        ("investigating", "Investigation In Progress"),
        ("resolved", "Resolved"),
        ("closed", "Closed"),
    ]

    PRIORITY_CHOICES = [
        ("standard", "Standard"),
        ("urgent", "Urgent"),
    ]

    PROPERTY_CHOICES = [
        ("residential", "Residential"),
        ("commercial", "Commercial"),
        ("industrial", "Industrial"),
        ("public", "Public Building"),
        ("other", "Other"),
    ]

    CONTACT_CHOICES = [
        ("email", "Email"),
        ("phone", "Phone"),
        ("post", "Post"),
    ]

    SURVEY_CHOICES = [
        ("required", "Required"),
        ("not_required", "Not Required"),
    ]

    STATUS_MESSAGES = {
        "submitted": "Your fault report has been submitted successfully.",
        "assigned": "An engineer has been assigned to your fault.",
        "investigating": "Our team is currently investigating the reported issue.",
        "resolved": "Your reported fault has been resolved.",
        "closed": "Your fault ticket has been closed.",
    }

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    reference_number = models.CharField(
        max_length=30,
        unique=True,
        blank=True
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="fault_reports"
    )

    # Step 1
    issue_type = models.CharField(max_length=100)

    is_business_customer = models.BooleanField(default=False)

    # Contact
    full_name = models.CharField(max_length=150)

    email = models.EmailField()

    phone = models.CharField(max_length=20)

    account_number = models.CharField(
        max_length=100,
        blank=True
    )

    # Address
    address = models.TextField()

    district = models.CharField(max_length=100)

    property_type = models.CharField(
        max_length=50,
        choices=PROPERTY_CHOICES
    )

    # Problem
    problem_description = models.TextField()

    related_issues = models.JSONField(
        default=list,
        blank=True
    )

    additional_notes = models.TextField(
        blank=True
    )

    preferred_contact = models.CharField(
        max_length=20,
        choices=CONTACT_CHOICES
    )

    survey_needed = models.CharField(
        max_length=20,
        choices=SURVEY_CHOICES
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="standard"
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="submitted"
    )

    engineer_notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.reference_number} - {self.issue_type}"

    def save(self, *args, **kwargs):

        is_new = self._state.adding

        previous_status = None

        if not is_new and self.pk:
            previous = FaultReport.objects.filter(pk=self.pk).first()

            if previous:
                previous_status = previous.status

        # Generate reference number
        if not self.reference_number:

            today = timezone.now().strftime("%Y%m%d")

            last_report = (
                FaultReport.objects.filter(
                    reference_number__startswith=f"ZB-{today}"
                )
                .order_by("-reference_number")
                .first()
            )

            if last_report:
                last_number = int(
                    last_report.reference_number.split("-")[-1]
                )
                next_number = last_number + 1
            else:
                next_number = 1

            self.reference_number = (
                f"ZB-{today}-{next_number:04d}"
            )

        super().save(*args, **kwargs)

        # Create timeline entry whenever status changes
        if (
            not is_new
            and previous_status
            and previous_status != self.status
        ):

            FaultStatusHistory.objects.create(
                fault=self,
                status=self.status,
                note=self.STATUS_MESSAGES.get(
                    self.status,
                    f"Status changed to {self.get_status_display()}",
                ),
            )


class FaultStatusHistory(models.Model):

    fault = models.ForeignKey(
        FaultReport,
        on_delete=models.CASCADE,
        related_name="timeline"
    )

    status = models.CharField(max_length=30)

    note = models.TextField(blank=True)

    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.fault.reference_number} - {self.status}"