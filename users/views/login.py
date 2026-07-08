from django.contrib.auth import authenticate
from rest_framework.views import APIView, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.views import TokenObtainPairView
from .JWT.jwt_serializer import JWTSerializer

from django.conf import settings


from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from django.conf import settings


class LoginUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {"error": "Both username and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh_token = RefreshToken.for_user(user)

        response = Response(
            {
                "user": user.get_username(),
                "access": str(refresh_token.access_token),
            },
            status=status.HTTP_200_OK
        )

        response.set_cookie(
            key='refresh_token',
            value=str(refresh_token),
            httponly=True,
            secure=not settings.DEBUG,
            samesite="Lax",
            path='/users/auth',
            max_age=int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()),
        )

        response.delete_cookie('guest_token', path='/')

        return response




class LoginUserViaJWT(TokenObtainPairView):
    serializer_class = JWTSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # login customization endpoint, I might use this later for logging/rate-limit

        return response