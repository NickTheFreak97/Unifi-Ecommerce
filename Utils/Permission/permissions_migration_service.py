from django.apps.registry import Apps
from django.db.models import Model
from users.models.user.roles import Role
from typing import Type

class PermissionsMigrationService:
    class GroupPermissionsMapper:
        def __init__(
            self,
            group: Type[Model],
            permissions: list[Model]
        ):
            self.group = group
            self.permissions = permissions

    @classmethod
    def extract_permissions_mapper(
        cls,
        apps: Apps,
        schema_editor,
        group_name: Role,
        permission_names: list[str],
        model_app: str,
        model_name: str
    ) -> GroupPermissionsMapper:
        Group = apps.get_model("auth", "Group")
        Permission = apps.get_model("auth", "Permission")
        ContentType = apps.get_model("contenttypes", "ContentType")

        group = Group.objects.get(name=group_name)
        content_type_for_model, _ = ContentType.objects.get_or_create(
            app_label=model_app,
            model=model_name.lower(),
        )

        all_permissions_codenames = [
            f"{permission_name}_{model_name.lower()}"
            for permission_name in permission_names
        ]

        all_permissions = list(
            Permission.objects.filter(
                content_type=content_type_for_model,
                codename__in=all_permissions_codenames
            )
        )

        return PermissionsMigrationService.GroupPermissionsMapper(
            group=group,
            permissions=all_permissions
        )


    @classmethod
    def add_permissions(
            cls,
            apps: Apps,
            schema_editor,
            group_name: Role,
            permission_names: list[str],
            model_app: str,
            model_name: str
    ) -> None:
        mapper = PermissionsMigrationService.extract_permissions_mapper(
            apps=apps,
            schema_editor=schema_editor,
            group_name=group_name,
            permission_names=permission_names,
            model_app=model_app,
            model_name=model_name
        )

        mapper.group.permissions.add(*mapper.permissions)

    @classmethod
    def remove_permissions(
        cls,
        apps: Apps,
        schema_editor,
        group_name: Role,
        permission_names: list[str],
        model_app: str,
        model_name: str
    ) -> None:
        mapper = PermissionsMigrationService.extract_permissions_mapper(
            apps=apps,
            schema_editor=schema_editor,
            group_name=group_name,
            permission_names=permission_names,
            model_app=model_app,
            model_name=model_name
        )

        mapper.group.permissions.remove(*mapper.permissions)
