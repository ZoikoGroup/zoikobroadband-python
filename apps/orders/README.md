# apps/orders — Django app for persisting BT Wholesale orders

Drop-in Django/DRF app that stores everything posted by the Next.js
`processOrderStripe()` flow (order metadata + full BT response) and accepts
BT's state-change webhook (API 8) for downstream lifecycle updates.

## Install

1. The `apps/orders/` folder lives inside your `apps/` package (sibling to `manage.py`).
2. Ensure `apps/` has an `__init__.py`, then add to `INSTALLED_APPS`:
   ```python
   INSTALLED_APPS = [
       # ...
       "rest_framework",
       "apps.orders",
   ]
   ```
3. Wire the URLs (root `urls.py`):
   ```python
   from django.urls import path, include
   urlpatterns = [
       # ...
       path("api/v1/", include("apps.orders.urls")),
   ]
   ```
4. Migrate:
   ```bash
   python manage.py migrate orders
   ```

The Next.js code already POSTs to `${NEXT_PUBLIC_API_BASE_URL}/api/v1/bqorders/`
— no client changes needed.

## Endpoints

| Method | Path                              | Purpose                                                  |
| ------ | --------------------------------- | -------------------------------------------------------- |
| POST   | `/api/v1/bqorders/`               | Create order (called by Next.js after BT 201/202).       |
| GET    | `/api/v1/bqorders/<external_id>/` | Retrieve order (e.g. for the Thank-You page).            |
| POST   | `/api/v1/bqorders/webhook/`       | BT Wholesale state-change notification landing zone (API 8). |

### Create — request shape

Matches `processOrderStripe(...).data` verbatim. The fields actually
required are `externalId`, `billingAddress.firstName`, `billingAddress.email`,
and a non-empty `cart`. Everything else is optional and stored in JSON
audit blobs (`cart_raw`, `bt_response_raw`, `request_payload_raw`, …).

### Create — response shape

```json
{
  "success": true,
  "message": "Order saved.",
  "data": {
    "id": 1,
    "external_id": "WC-1736342400000-12345",
    "bt_order_id": "ORD-987654321",
    "local_status": "created",
    "bt_state": "acknowledged",
    "email": "alice@example.com",
    "...": "..."
  }
}
```

If the same `externalId` is POSTed twice (network retry), the second call
returns `200` with `duplicate: true` and the existing record — no duplicate
rows are created.

### Webhook

Configure BT Wholesale to send `ProductOrderStateChangeEvent` to
`POST /api/v1/bqorders/webhook/`. The handler always responds 200 (BT
retries on non-2xx) and persists the event even when the `externalId`
isn't in the database yet — those events can be reconciled with:

```bash
python manage.py reconcile_bt_webhooks
python manage.py reconcile_bt_webhooks --dry-run  # preview first
```

## Data model

- **`BTOrder`** — one row per checkout. Denormalised columns for
  customer/service/product/appointment/totals are indexed for admin filtering;
  full input is preserved in JSON `*_raw` fields for replay and audit.
- **`BTOrderEvent`** — append-only log. Sources are `checkout`, `webhook`,
  `manual`, `system`. Never overwritten.

## Admin

Both models are registered. `BTOrder` has a coloured BT-state badge in the
list view, full-text search across the key identifiers, and inline display
of all related events. Raw JSON blobs are collapsed by default.

## Local statuses vs BT states

| Field          | Source                | Values                                              |
| -------------- | --------------------- | --------------------------------------------------- |
| `local_status` | Set on creation       | `created` (201), `pending` (202), `unknown`, `failed` |
| `bt_state`     | Updated by webhook    | `acknowledged`, `inProgress`, `held`, `completed`, `refused`, `cancelled`, `rejected` |

The two are intentionally separate: `local_status` describes how the order
reached us; `bt_state` describes where BT is in its lifecycle.

## Notes for production

- **Auth**: the create + webhook endpoints are open by default
  (`AllowAny`) because Next.js calls server-to-server and BT calls without a
  user. Lock them down with a shared secret header or mTLS in front of the
  app — at minimum, check `Authorization: Bearer <shared-secret>` in
  `BTOrderCreateView.post` and verify BT's `apigw-client-id` on the webhook.
- **Idempotency**: enforced via the unique constraint on `external_id`.
- **No retries on the webhook side**: we return 200 even for malformed
  payloads to avoid BT's retry storm; check the logs for invalid events.
- **PII**: billing data is denormalised onto `BTOrder`. Add encryption-at-rest
  on the DB tablespace or use Django's `EncryptedFields` if your compliance
  posture requires it.
