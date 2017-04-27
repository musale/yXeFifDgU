"""Accounts admin."""
from __future__ import unicode_literals

from django.contrib import admin

from loyalty.apps.account import models


class UserProfileAdmin(admin.ModelAdmin):
    """UserProfile admin class."""

    pass


admin.site.register(models.UserProfile, UserProfileAdmin)
