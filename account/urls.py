from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'account'
urlpatterns = [
    path('auth/user/', CurrentUserView.as_view(), name='current_user'),
    path('signin/', SigninView.as_view(), name='login'),
    path('verify_code/', VerifyCodeView.as_view(), name='verify_code'),
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    ]