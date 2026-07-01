from django.urls import path
from .views import RegisterCustomer, LogoutUser, RegisterStaffMember, CookieTokenRefreshView, WhoAmI, ListAllUsersByGroup
from .views.login import LoginUserViaJWT

urlpatterns = [
    path('register_customer/', RegisterCustomer.as_view(), name='register_customer'),
    path('register_staff/', RegisterStaffMember.as_view(), name='register_staff'),
    path('auth/login/', LoginUserViaJWT.as_view(), name='login'),
    path('auth/logout/', LogoutUser.as_view(), name='logout'),
    path('auth/token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('auth/who_am_i/', WhoAmI.as_view(), name='who_am_i'),
    path('list_users_by_group/', LogoutUser.as_view(), name='logout'),
]

