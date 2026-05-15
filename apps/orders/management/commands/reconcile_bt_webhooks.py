"""
Reconcile orphaned BT webhook events with their orders.

Orphans happen when BT sends a state-change notification before
processOrderStripe returns and writes the row — or if the Next.js POST to
this endpoint fails on the first attempt. The webhook handler always stores
the event (with `order=NULL` and the external_id preserved), so we can fix
the linkage retroactively.

Run manually or on a cron:
    python manage.py reconcile_bt_webhooks
"""

from django.core.management.base import BaseCommand

from apps.orders.models import BTOrder, BTOrderEvent, BTOrderState


class Command(BaseCommand):
    help = "Link orphaned BTOrderEvent rows (order=NULL) to their BTOrder."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Print what would be linked without writing.",
        )

    def handle(self, *args, **opts):
        dry = opts["dry_run"]
        orphans = BTOrderEvent.objects.filter(order__isnull=True).exclude(external_id="")
        total = orphans.count()
        self.stdout.write(f"Found {total} orphaned event(s).")

        linked = 0
        for ev in orphans.iterator():
            order = BTOrder.objects.filter(external_id=ev.external_id).first()
            if not order:
                continue

            if dry:
                self.stdout.write(
                    f"  would link event #{ev.pk} ({ev.event_type}) → order #{order.pk}"
                )
            else:
                ev.order = order
                ev.save(update_fields=["order"])

                # Replay the state advance if needed.
                if ev.state and ev.state in BTOrderState.values:
                    order.advance_state(ev.state)

                self.stdout.write(
                    f"  linked event #{ev.pk} ({ev.event_type}) → order #{order.pk}"
                )
            linked += 1

        suffix = " (dry-run)" if dry else ""
        self.stdout.write(self.style.SUCCESS(f"Linked {linked}/{total}{suffix}."))
