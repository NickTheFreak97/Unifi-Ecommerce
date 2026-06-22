from Utils import PermissionsMigrationService
from users.models.user.roles import Role
from django.db import migrations


def AddPaymentMethodPermissions(apps, schema_editor):
    all_base_permissions = ["add", "change", "view", "delete"]

    permissionsTable = {
        Role.webmaster: all_base_permissions,
        Role.staff: all_base_permissions,
        Role.customer: ['view']
    }

    for role in permissionsTable:
        PermissionsMigrationService.add_permissions(
            apps=apps,
            schema_editor=schema_editor,
            group_name=role,
            permission_names=permissionsTable[role],
            model_app='payment',
            model_name='PaymentMethod'
        )


def RemovePaymentMethodPermissions(apps, schema_editor):
    all_base_permissions = ["add", "change", "view", "delete"]

    permissionsTable = {
        Role.webmaster: all_base_permissions,
        Role.staff: all_base_permissions,
        Role.customer: ['view']
    }

    for role in permissionsTable:
        PermissionsMigrationService.remove_permissions(
            apps=apps,
            schema_editor=schema_editor,
            group_name=role,
            permission_names=permissionsTable[role],
            model_app='payment',
            model_name='PaymentMethod'
        )



class Migration(migrations.Migration):
    dependencies = [
        ('payment', '0002_paymentintent_payment'),
    ]

    operations = [
        migrations.RunPython(AddPaymentMethodPermissions, RemovePaymentMethodPermissions),
    ]