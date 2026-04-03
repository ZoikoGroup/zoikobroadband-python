from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PlanCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True, verbose_name="Name")),
                ("slug", models.SlugField(blank=True, max_length=120, unique=True, verbose_name="Slug")),
                ("description", models.TextField(blank=True, verbose_name="Description")),
                ("is_active", models.BooleanField(default=True, verbose_name="Active")),
                ("sort_order", models.PositiveIntegerField(default=0, verbose_name="Sort Order")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Plan Category",
                "verbose_name_plural": "Plan Categories",
                "ordering": ["sort_order", "name"],
            },
        ),
        migrations.CreateModel(
            name="Plan",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="plans",
                        to="plans.plancategory",
                        verbose_name="Category",
                    ),
                ),
                ("name", models.CharField(max_length=200, verbose_name="Plan Name")),
                ("slug", models.SlugField(blank=True, max_length=220, unique=True, verbose_name="Plan Slug")),
                ("bt_plan_id", models.CharField(blank=True, max_length=100, verbose_name="BT Plan ID")),
                ("bt_plan_name", models.CharField(blank=True, max_length=200, verbose_name=" BT Plan Name")),
                ("description", models.TextField(blank=True, verbose_name="Description")),
                ("is_active", models.BooleanField(default=True, verbose_name="Active")),
                ("is_featured", models.BooleanField(default=False, verbose_name="Featured")),
                ("sort_order", models.PositiveIntegerField(default=0, verbose_name="Sort Order")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Plan",
                "verbose_name_plural": "Plans",
                "ordering": ["sort_order", "name"],
            },
        ),
        migrations.CreateModel(
            name="PlanVariation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "plan",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="variations",
                        to="plans.plan",
                        verbose_name="Plan",
                    ),
                ),
                ("label", models.CharField(max_length=100, verbose_name="Label")),
                (
                    "duration_value",
                    models.PositiveIntegerField(
                        default=1,
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="Duration",
                    ),
                ),
                (
                    "duration_unit",
                    models.CharField(
                        choices=[
                            ("day", "Day(s)"),
                            ("week", "Week(s)"),
                            ("month", "Month(s)"),
                            ("year", "Year(s)"),
                        ],
                        default="month",
                        max_length=10,
                        verbose_name="Duration Unit",
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Price",
                    ),
                ),
                ("currency", models.CharField(default="USD", max_length=3, verbose_name="Currency")),
                (
                    "discount_percentage",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=5,
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Discount %",
                    ),
                ),
                ("bt_plan_id", models.CharField(blank=True, max_length=100, verbose_name="BT Plan ID")),
                ("is_active", models.BooleanField(default=True, verbose_name="Active")),
                ("is_default", models.BooleanField(default=False, verbose_name="Default Variation")),
                ("sort_order", models.PositiveIntegerField(default=0, verbose_name="Sort Order")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Plan Variation",
                "verbose_name_plural": "Plan Variations",
                "ordering": ["sort_order", "price"],
            },
        ),
    ]
