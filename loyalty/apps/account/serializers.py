"""Serializer classes."""
from django.contrib.auth.models import User
from rest_framework import serializers

from loyalty.apps.account import models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """User seriliazer."""

    class Meta:
        """Serializer meta data."""

        model = User
        fields = ("username", "first_name", "last_name", "email")


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    """User Profile serializer."""

    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')

    class Meta:
        """Serializer meta data."""

        model = models.UserProfile
        fields = (
            "username", "first_name", "last_name", "email", "user_type",
            "phonenumber", "avatar",  "gender", "date_joined", "pk")
        depth = 1
