from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import logout
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

"""
To test this class in Postman I had to
    - Login with a user
    - You get the refresh token in the response
    - In the Authorization tab: Bearer token: {access_token}, in body add key: "refresh": "{refresh_token}"
"""
class LogoutUser(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = RefreshToken(request.COOKIES.get('refresh_token'))
            refresh_token.blacklist()
        except TokenError:
            return Response(
                {
                    "detail": "Invalid, blacklisted or missing refresh token."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        logout(request)

        response = Response(
            {
                "detail": "success"
            },
            status=status.HTTP_205_RESET_CONTENT
        )

        response.delete_cookie('refresh_token', path='/users/auth')

        return response