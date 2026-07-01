from collections import defaultdict

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import Group
from users.models.user.user import User

class ListAllUsersByGroup(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        groupings: defaultdict = defaultdict()
        for group in Group.objects.all():
            if groupings[group.name] is None:
                groupings[group.name] = []

            for user in User.objects.filter(groups=group):
                groupings[group.name].append(user.id)

        return Response(
            {
                'users_grouped_by_group': groupings,
            },
            status=status.HTTP_200_OK,
        )
