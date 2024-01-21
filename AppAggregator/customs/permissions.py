from rest_framework.permissions import IsAuthenticated

from app_aggregator.model_choices import UserTypes


class IsAggregatorAuthenticated(IsAuthenticated):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.type == UserTypes.AGGREGATOR)


class IsSuperUser(IsAuthenticated):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)
