from django.urls import path
from JWTRefreshCookie import CookieTokenRefreshView
from WhoAmI import WhoAmI
from .views import RegisterCustomer, LogoutUser, RegisterStaffMember
from .views.login import LoginUserViaJWT

urlpatterns = [
    path('register_customer/', RegisterCustomer.as_view(), name='register_customer'),
    path('register_staff/', RegisterStaffMember.as_view(), name='register_staff'),
    path('auth/login/', LoginUserViaJWT.as_view(), name='login'),
    path('auth/logout/', LogoutUser.as_view(), name='logout'),
    path('auth/token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('auth/who_am_i', WhoAmI.as_view(), name='who_am_i'),
]

