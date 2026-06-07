"""
Drop BTOrder.bt_response_raw.

The raw response returned by BT's /productOrder endpoint is no longer
persisted to the database — only the derived fields (bt_order_id,
local_status, appointment_*) are kept on the row. Order-creation events
in BTOrderEvent likewise no longer carry the raw BT response in their
payload_raw column; existing event rows are left untouched.
"""

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="btorder",
            name="bt_response_raw",
        ),
    ]
