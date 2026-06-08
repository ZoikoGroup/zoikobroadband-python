from django.db import models


class BusinessBroadbandInquiry(models.Model):

    BUSINESS_SIZE_CHOICES = [
        ('1-10 employees', '1-10 employees'),
        ('11-50 employees', '11-50 employees'),
        ('50+ employees', '50+ employees'),
    ]

    business_name = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255)

    email = models.EmailField()
    phone_number = models.CharField(max_length=20)

    business_postcode = models.CharField(max_length=20)

    business_size = models.CharField(
        max_length=50,
        choices=BUSINESS_SIZE_CHOICES
    )

    additional_requirements = models.TextField(
        blank=True,
        null=True
    )

    email_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name