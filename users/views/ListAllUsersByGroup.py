from collections import defaultdict
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models.user.user import User


class ListAllUsersByGroup(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        groupings = defaultdict(list)

        for group in Group.objects.all():
            for user in User.objects.filter(groups=group):
                groupings[group.name].append(
                    {
                        "id": user.id,
                        "username": user.username
                    }
                )

        return Response(
            {
                "users_grouped_by_group": dict(groupings),
            },
            status=status.HTTP_200_OK,
        )