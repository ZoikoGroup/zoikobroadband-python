# Plans Module

A Django app for managing variable subscription plans with duration-based pricing variations and  integration.

---

## Structure

```
apps/plans/
├── __init__.py
├── apps.py
├── models.py          # PlanCategory, Plan, PlanVariation
├── admin.py           # Tabbed admin with inline variations
├── serializers.py     # DRF serializers
├── views.py           # ReadOnly ViewSets
├── urls.py            # Router-based URL config
├── migrations/
│   └── 0001_initial.py
└── static/plans/admin/
    ├── plan_tabs.css
    └── plan_tabs.js
```

---

## Setup

### 1. Add to INSTALLED_APPS

```python
# core/settings.py
INSTALLED_APPS = [
    ...
    "apps.plans",
]
```

### 2. Add URL routes

```python
# core/urls.py
from django.urls import path, include

urlpatterns = [
    ...
    path("api/plans/", include("apps.plans.urls", namespace="plans")),
]
```

### 3. Run migrations

```bash
python manage.py migrate
```

### 4. Collect static (for admin tab UI)

```bash
python manage.py collectstatic
```

---

## Models

### `PlanCategory`
Groups plans logically (e.g., Basic, Pro, Enterprise).

| Field | Description |
|---|---|
| `name` | Display name |
| `slug` | Auto-generated URL slug |
| `is_active` | Toggle visibility |
| `sort_order` | Admin ordering |

---

### `Plan`
The main plan entity. Contains  integration fields.

| Field | Description |
|---|---|
| `name` | Plan display name |
| `slug` | Unique URL slug (auto-generated) |
| `bt_plan_id` | BT Plan ID |
| `bt_plan_name` |  BT Plan Name |
| `category` | FK → PlanCategory |
| `is_featured` | Highlight in UI |

---

### `PlanVariation`
Each plan can have multiple variations with different durations and prices.

| Field | Description |
|---|---|
| `label` | e.g., "Monthly", "Annual" |
| `duration_value` | Numeric value (e.g., 1, 3, 12) |
| `duration_unit` | `day` / `week` / `month` / `year` |
| `price` | Base price |
| `currency` | ISO currency code (default: USD) |
| `discount_percentage` | Optional promo discount |
| `bt_plan_id` | Override BTBT Plan ID (falls back to parent) |
| `is_default` | Mark as recommended option |

---

## Admin UI

The Plan change form uses a **2-tab layout**:

- **⚙ General** — Plan name, slug, BTBT Plan ID/Name, category, status
- **📦 Plan Variations** — Inline tabular editor for all duration/price variations

Tab switching is handled by `plan_tabs.js` — no extra dependencies needed.

---

## API Endpoints

| Method | URL | Description |
|---|---|---|
| GET | `/api/plans/` | List all active plans |
| GET | `/api/plans/{slug}/` | Plan detail |
| GET | `/api/plans/{slug}/variations/` | Variations for a plan |
| GET | `/api/plans/categories/` | List categories with plans |
| GET | `/api/plans/variations/` | All active variations |

### Filter examples

```
GET /api/plans/?category__slug=professional
GET /api/plans/?is_featured=true
GET /api/plans/variations/?duration_unit=month
GET /api/plans/variations/?plan__slug=pro-plan&is_default=true
```

---

##  Integration

`bt_plan_id` and `bt_plan_name` live on the `Plan` model and correspond to your  Subscription Plan.

If a `PlanVariation` has its own `bt_plan_id` set, that takes precedence. Otherwise it inherits from the parent `Plan`. Use `variation.effective_bt_plan_id` to always get the correct value.

```python
variation = PlanVariation.objects.get(pk=1)
plan_id = variation.effective_bt_plan_id  # variation-level or inherited
```
