from django.contrib.auth import get_user_model

from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from api.models import Subscriber

User = get_user_model()


class SpecialUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )


class SpecialUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Subscriber.objects.filter(
            user=user,
            author=obj
        ).exists()
