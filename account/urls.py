from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import *


app_name = 'account'
urlpatterns = [
    path('signin/', SigninView.as_view(), name='login'),
    path('verify_code/', VerifyCodeView.as_view(), name='verify_code'),
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('api_token_auth/', obtain_auth_token, name='api_token_auth'),
]