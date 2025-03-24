from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import *


app_name = 'account'
urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('api_token_auth/', obtain_auth_token, name='api_token_auth'),
]