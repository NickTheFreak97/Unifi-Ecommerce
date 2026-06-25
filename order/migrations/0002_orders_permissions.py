from django.db.migrations import RunPython
from django.db import migrations
from django.contrib.auth.management import create_permissions, create_contenttypes
from django.apps import apps as global_apps
from users.models.user.roles import Role
from Utils import PermissionsMigrationService

def apply_permissions(apps, schema_editor):
    create_permissions(global_apps.get_app_config('order'), verbosity=0, apps=apps)
    create_contenttypes(global_apps.get_app_config('order'), verbosity=0)

    orders_permissions = {
        Role.webmaster: ['view', 'change', 'delete', 'add'],
        Role.staff: ['view', 'change', 'delete', 'add'],
        Role.customer: ['view', 'change', 'delete', 'add'],
    }

    for role in orders_permissions:
        PermissionsMigrationService.add_permissions(
            apps=apps,
            schema_editor=schema_editor,
            group_name=role,
            permission_names=orders_permissions[role],
            model_app='order',
            model_name='order'
        )

def remove_permissions(apps, schema_editor):
    orders_permissions = {
        Role.webmaster: ['view', 'change', 'delete', 'add'],
        Role.staff: ['view', 'change', 'delete', 'add'],
        Role.customer: ['view', 'change', 'delete', 'add'],
    }

    for role in orders_permissions:
        PermissionsMigrationService.remove_permissions(
            apps=apps,
            schema_editor=schema_editor,
            group_name=role,
            permission_names=orders_permissions[role],
            model_app='order',
            model_name='order'
        )


class Migration(migrations.Migration):
    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        RunPython(apply_permissions, remove_permissions),
    ]