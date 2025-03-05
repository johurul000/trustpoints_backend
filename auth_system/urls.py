from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView
from .views import *

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('get-user/', GetUserAPIView.as_view(), name='get-user'),
    path('users/<int:user_id>/edit/', EditUserAPIView.as_view(), name='edit_user_details'),

    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_view'),

    path('admin/login/', AdminLoginAPIView.as_view(), name='admin_login'),
    path("admin/edit/<int:admin_id>/", EditAdminAPIView.as_view(), name="edit-admin"),
    path("admin/me/", GetAdminAPIView.as_view(), name="get-admin"),

]
