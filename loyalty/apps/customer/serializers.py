"""Seriliazer class for Customer app models."""
from rest_framework import serializers

from loyalty.apps.account import models


class CustomerModelSerializer(serializers.ModelSerializer):
    """Serializer for Customer model."""

    class Meta:
        """Serializer meta data."""

        model = models.Customer
        fields = (
            "owner", "first_name", "last_name", "phonenumber", "gender",
            "loyalty_account", "date_of_birth", "date_joined", "pk")
