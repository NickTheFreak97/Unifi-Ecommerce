from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

"""
To test this class in Postman I had to
    - Login with a user
    - You get the refresh token in the response
    - In the Authorization tab: Bearer token: {access_token}, in body add key: "refresh": "{refresh_token}"
"""
class LogoutUser(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = RefreshToken(request.data.get("refresh"))
        refresh_token.blacklist()

        response = Response(
            {
                "detail": "success"
            },
            status=status.HTTP_205_RESET_CONTENT
        )

        response.delete_cookie('refresh_token', path='/users/auth')

        return response