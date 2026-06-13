from django.db.models import Q
from django.contrib.auth.models import Group
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from users.models.user.user import User
from users.models.user.roles import Role

class RegisterCustomer(APIView):
    def post(self, request):
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')

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

                    customer_group = Group.objects.get(name=Role.customer)
                    created_user.groups.add(customer_group)

                    return Response({
                        'success': 'created a new user',
                        'id': created_user.id
                        },
                        status=status.HTTP_201_CREATED
                    )