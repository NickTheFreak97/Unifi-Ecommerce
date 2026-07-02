from django.db.models import Q
from django.contrib.auth.models import Group
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from users.models.user.user import User
from users.models.user.roles import Role
from django.conf import settings


def __create_user__(email, username, password):
    if not email or not username or not password:
        return Response(
            {
                'error': 'username, password and email are required',
                'username': username,
                'email': email,
                'password': password
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    else:
        if len(email) <= 0 or len(username) <= 0 or len(password) <= 0:
            return Response(
                {
                    'error': 'username, password and email cannot be blank',
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            if User.objects.filter(Q(email=email) | Q(username=username)).exists():
                return Response(
                    {'error': 'email already exists'},
                    status=status.HTTP_409_CONFLICT
                )
            else:
                created_user = User.objects.create_user(
                    email=email,
                    username=username,
                    password=password
                )

                return created_user

class RegisterCustomer(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        created_user = __create_user__(
            request.data.get('email'),
            request.data.get('username'),
            request.data.get('password')
        )

        if isinstance(created_user, User):
            customer_group = Group.objects.get(name=Role.customer)
            created_user.groups.add(customer_group)

            token_for_new_user = RefreshToken.for_user(created_user)
            response = Response({
                'success': 'created a new user',
                'id': created_user.id,
                "access": str(token_for_new_user.access_token),
                },
                status=status.HTTP_201_CREATED
            )

            response.set_cookie(
                key='refresh_token',
                value=str(token_for_new_user),
                httponly=True,
                secure=not settings.DEBUG,
                samesite="Lax",
                path='/users/auth',
                max_age=int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()),
            )

            return response
        else:
            return created_user


class RegisterStaffMember(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        created_user = __create_user__(
            request.data.get('email'),
            request.data.get('username'),
            request.data.get('password')
        )

        if isinstance(created_user, User):
            staff_group = Group.objects.get(name=Role.staff)
            created_user.groups.add(staff_group)

            token_for_new_user = RefreshToken.for_user(created_user)
            response = Response({
                'success': 'created a new staff member',
                'id': created_user.id,
                "access": str(token_for_new_user.access_token),
            },
                status=status.HTTP_201_CREATED
            )

            response.set_cookie(
                key='refresh_token',
                value=str(token_for_new_user),
                httponly=True,
                secure=not settings.DEBUG,
                samesite="Lax",
                path='/users/auth',
                max_age=int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()),
            )

            return response
        else:
            return created_user