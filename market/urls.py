from django.urls import path
from account import views as account_views
from . import views as market_views
from rest_framework.authtoken.views import obtain_auth_token


app_name = 'market'

urlpatterns = [
    path('signup/', account_views.SignupAPIView.as_view(), name='signup'),
    path('logout/', account_views.LogoutAPIView.as_view(), name='logout'),
    path('api_token_auth/', obtain_auth_token, name='api_token_auth'),

    path('products/', market_views.ProductListAPIView.as_view(), name='products'),
    path('products/<pk>', market_views.ProductListAPIView.as_view(), name='products'),


]