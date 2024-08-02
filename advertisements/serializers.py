from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(read_only=True)

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator', 'status', 'created_at')

    def create(self, validated_data):
        """Метод для создания"""

        # Получаем текущего пользователя из контекста
        user = self.context['request'].user

        # Устанавливаем текущего пользователя как создателя объявления
        validated_data['creator'] = user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        user = self.context['request'].user

        if self.instance is None:
            # Проверяем только при создании, так как обновление может изменять статус на закрытый
            open_ads_count = Advertisement.objects.filter(creator=user, status='OPEN').count()
            if open_ads_count >= 10:
                raise ValidationError('У вас не может быть больше 10 открытых объявлений.')

        else:
            # При обновлении проверяем, не превышает ли пользователь лимит
            open_ads_count = Advertisement.objects.filter(creator=user, status='OPEN').exclude(
                id=self.instance.id).count()
            if data.get('status') == 'OPEN' and open_ads_count >= 10:
                raise ValidationError('У вас не может быть больше 10 открытых объявлений.')

        return data