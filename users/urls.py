from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterCustomer, LogoutUser
from .views.login import LoginUserViaJWT

urlpatterns = [
    path('register_customer/', RegisterCustomer.as_view(), name='register_customer'),
    path('register_staff/', RegisterCustomer.as_view(), name='register_staff'),
    path('login/', LoginUserViaJWT.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

