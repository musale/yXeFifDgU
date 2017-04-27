"""Customers admin."""
from __future__ import unicode_literals

from django.contrib import admin

from loyalty.apps.account import models


class CustomerModelAdmin(admin.ModelAdmin):
    """Customer admin class."""

    pass


admin.site.register(models.Customer, CustomerModelAdmin)
