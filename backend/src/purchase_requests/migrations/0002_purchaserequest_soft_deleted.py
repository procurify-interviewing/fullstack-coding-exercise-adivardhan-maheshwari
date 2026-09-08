from django.db import migrations, models
from django.utils import timezone


def set_soft_deleted(apps, schema_editor):
    PurchaseRequest = apps.get_model("purchase_requests", "PurchaseRequest")
    PurchaseRequest.objects.filter(deleted_at__isnull=False).update(soft_deleted=True)


def set_deleted_at(apps, schema_editor):
    # The original deletion timestamp is not recoverable from a boolean.
    PurchaseRequest = apps.get_model("purchase_requests", "PurchaseRequest")
    PurchaseRequest.objects.filter(soft_deleted=True).update(deleted_at=timezone.now())


class Migration(migrations.Migration):

    dependencies = [
        ("purchase_requests", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="purchaserequest",
            name="soft_deleted",
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(set_soft_deleted, set_deleted_at),
        migrations.RemoveField(
            model_name="purchaserequest",
            name="deleted_at",
        ),
    ]
