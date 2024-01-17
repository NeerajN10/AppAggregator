from django.db import transaction
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from AppAggregator.customs.permissions import IsAggregatorAuthenticated
from AppAggregator.customs.viewsets import CustomModelViewSet
from app_aggregator.models import AppData, UserPurchasedApps
from app_aggregator.serializers import AppDataSerializer, UserPurchasedAppsSerializer


class AppDataViewSet(CustomModelViewSet):
    queryset = AppData.objects.all()
    serializer_class = AppDataSerializer
    permission_classes = [IsAggregatorAuthenticated]

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        name = instance.name
        # check if any user has purchased this app
        if instance.user_apps.exists():
            return Response(data="Cannot delete. Some Users have purchased this app",
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        instance.delete()
        return Response(data=f'{name} deleted successfully!', status=status.HTTP_200_OK)

    @action(methods=['PATCH'], detail=True, url_name='ban_app')
    def ban_app(self, request, pk=None):
        app = self.get_object()
        app.active = False
        app.save(update_fields=('active',))
        return Response(data=f"Successfully Banned {app.name}", status=status.HTTP_200_OK)

    @action(methods=['PATCH'], detail=True, url_name='unban_app')
    def unban_app(self, request, pk=None):
        app = self.get_object()
        app.active = True
        app.save(update_fields=('active',))
        return Response(data=f"Successfully Unbanned {app.name}", status=status.HTTP_200_OK)


class AppListViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = AppData.objects.filter(active=True).all()
    serializer_class = AppDataSerializer
    permission_classes = [IsAuthenticated]


class UserPurchasesViewSet(CustomModelViewSet):
    queryset = UserPurchasedApps.objects.all()
    serializer_class = UserPurchasedAppsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        self.queryset = self.queryset.filter(user=self.request.user).all()
        return self.queryset

    @action(methods=['PATCH'], detail=True, url_name='archive_purchase')
    def archive_purchase(self, request, pk=None):
        purchase = self.get_object()
        purchase.active = False
        purchase.save(update_fields=('active',))
        return Response(data=f"Successfully Archived {purchase.app.name}", status=status.HTTP_200_OK)

    @action(methods=['PATCH'], detail=True, url_name='unarchive_purchase')
    def unarchive_purchase(self, request, pk=None):
        purchase = self.get_object()
        purchase.active = True
        purchase.save(update_fields=('active',))
        return Response(data=f"Successfully Unarchived {purchase.app.name}", status=status.HTTP_200_OK)

    @action(methods=['DELETE'], detail=True, url_name='delete_purchase')
    def delete_purchase(self, request, pk=None):
        purchase = self.get_object()
        purchase.delete()
        return Response(data=f"Successfully Deleted {purchase.app.name}", status=status.HTTP_200_OK)
