from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app_aggregator.viewsets import AppDataViewSet, AppListViewSet, UserPurchasesViewSet, UserViewSet

app_agg_router = DefaultRouter()

app_agg_router.register('app_data', AppDataViewSet, basename='app_data')
app_agg_router.register('active_apps', AppListViewSet, basename='active_apps')
app_agg_router.register('user_purchases', UserPurchasesViewSet, basename='user_purchases')
app_agg_router.register('user', UserViewSet, basename='user_data_upload')

urlpatterns = [
    path('app/', include(app_agg_router.urls))
]
