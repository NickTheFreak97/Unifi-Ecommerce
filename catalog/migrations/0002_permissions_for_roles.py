from django.db import migrations
from django.apps import apps as global_apps
from django.contrib.auth.management import create_permissions, create_contenttypes
from users.models.user.roles import Role
from Utils import PermissionsMigrationService

def create_groups_permissions(apps, schema_editor):
    create_permissions(global_apps.get_app_config('catalog'), verbosity=0, apps=apps)
    create_contenttypes(global_apps.get_app_config('catalog'), verbosity=0)

    models_to_alter = [ 'product', 'productvariant', 'productattribute', 'category' ]

    product_permissions = {
        Role.webmaster: ['view', 'change', 'delete', 'add'],
        Role.staff: ['view', 'change', 'delete', 'add'],
        Role.customer: ['view'],
    }

    for role in product_permissions:
        permissions_for_this_role = product_permissions[role]

        for model in models_to_alter:
            PermissionsMigrationService.add_permissions(
                apps=apps,
                schema_editor=schema_editor,
                group_name=role,
                permission_names=permissions_for_this_role,
                model_app='catalog',
                model_name=model
            )


def reverse_migration(apps, schema_editor):
    models_to_alter = ['product', 'productvariant', 'productattribute', 'category']

    product_permissions = {
        Role.webmaster: ['view', 'change', 'delete', 'add'],
        Role.staff: ['view', 'change', 'delete', 'add'],
        Role.customer: ['view'],
    }

    for role in product_permissions:
        permissions_for_this_role = product_permissions[role]

        for model in models_to_alter:
            PermissionsMigrationService.remove_permissions(
                apps=apps,
                schema_editor=schema_editor,
                group_name=role,
                permission_names=permissions_for_this_role,
                model_app='catalog',
                model_name=model
            )


class Migration(migrations.Migration):
    initial = False

    dependencies = [
        ('users', '0001_create_groups'),
        ('catalog', '0001_make_products_models')
    ]

    operations = [
        migrations.RunPython(create_groups_permissions, reverse_migration),
    ]
