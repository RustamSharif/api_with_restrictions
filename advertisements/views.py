from rest_framework import permissions, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from advertisements.models import Advertisement
from advertisements.serializers import AdvertisementSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Только автор объявления может изменить или удалить его
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.creator == request.user


class AdvertisementViewSet(viewsets.ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        """Создание объекта."""
        serializer.save(creator=self.request.user)

    def update(self, request, *args, **kwargs):
        # Проверка что пользователь автор объявления
        advertisement = self.get_object()
        if advertisement.creator != request.user:
            raise PermissionDenied('You do not have permission to modify this advertisement.')
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Проверка что пользователь автор объявления
        advertisement = self.get_object()
        if advertisement.creator != request.user:
            raise PermissionDenied('You do not have permission to delete this advertisement.')
        return super().destroy(request, *args, **kwargs)

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]