from django.urls import path
from account import views
from rest_framework.authtoken.views import obtain_auth_token


app_name = 'market'

urlpatterns = [
    path('signup/', views.SignupAPIView.as_view(), name='signup'),
    path('api_token_auth/', obtain_auth_token, name='api_token_auth'),


]