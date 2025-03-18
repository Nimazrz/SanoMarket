from django.urls import path, include
from account import views as account_views
from . import views as market_views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'products', market_views.ProductsViewSet, basename='products')

app_name = 'market'

urlpatterns = [
    path('signup/', account_views.SignupAPIView.as_view(), name='signup'),
    path('logout/', account_views.LogoutAPIView.as_view(), name='logout'),
    path('api_token_auth/', obtain_auth_token, name='api_token_auth'),

    path('', include(router.urls)),



]