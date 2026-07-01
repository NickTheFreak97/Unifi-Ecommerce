from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

class CookieTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        raw_refresh = request.COOKIES.get('refresh_token')
        if raw_refresh is None:
            return Response(
                {
                    "error": "You cannot refresh a token that doesn't exist."
                }, status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = self.get_serializer(data={ "refresh": raw_refresh })

        try:
            serializer.is_valid(raise_exception=True)
        except (TokenError, InvalidToken):
            return Response(
                {
                    "error": "Either the token was not valid or it's blacklisted."
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        data = serializer.validated_data
        response = Response(
            {
                "access": data["access"]
            },
            status=status.HTTP_200_OK
        )

        if "refresh" in data:
            response.set_cookie(
                key='refresh_token',
                value=data["refresh"],
                httponly=True,
                secure=not settings.DEBUG,
                samesite="Lax",
                path='/users/auth',
                max_age=int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()),
            )

        return response