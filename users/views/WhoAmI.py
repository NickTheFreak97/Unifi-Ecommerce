from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

class WhoAmI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_authenticated:
            return Response(
                {
                    'id': request.user.id,
                    'email': request.user.email,
                    'username': request.user.username,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
            )