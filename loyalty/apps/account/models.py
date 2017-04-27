"""User account models."""
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now


def upload_to(instance, filename):
    """Callable method to store an avatar."""
    # file will be uploaded to MEDIA_ROOT/avatars/<username>/<filename>
    return "avatars/{0}/{1}".format(instance.user.username, filename)


GENDERS = (
    ("MALE", "MALE"),
    ("FEMALE", "FEMALE")
)

USER_TYPES = (
    ("ADMIN", "ADMIN"),
    ("SHOPKEEPER", "SHOPKEEPER")
)


class UserProfile(models.Model):
    """A user profile for the admins and shopkeepers."""

    user = models.OneToOneField(User)
    user_type = models.CharField(
        max_length=10, choices=USER_TYPES, default=USER_TYPES[0][0])
    phonenumber = models.CharField(max_length=20)
    activation_key = models.CharField(max_length=40, null=True, blank=True)
    key_expiry_date = models.DateTimeField(null=True, default=now)
    avatar = models.ImageField(
        upload_to=upload_to, default="avatars/default-avatar.png")
    gender = models.CharField(
        max_length=10, choices=GENDERS, default=GENDERS[0][0], null=True,
        blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Object return string."""
        return "{0}: {1}".format(self.gender, self.user.get_full_name())

    class Meta:
        """Meta data class."""

        ordering = ['-id']


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Signal post_save."""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Signal post_save."""
    instance.userprofile.save()


class Customer(models.Model):
    """A customer object."""

    owner = models.ForeignKey(UserProfile)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    phonenumber = models.CharField(max_length=20)
    gender = models.CharField(
        max_length=10, choices=GENDERS, default=GENDERS[0][0], null=True,
        blank=True)
    loyalty_account = models.CharField(
        max_length=40, null=True, blank=True, unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Object return string."""
        return "{2}:{0} {1}".format(self.firstname, self.lastname, self.gender)

    class Meta:
        """Meta data class."""

        ordering = ['-id']

    def get_full_name(self):
        """Get customer full name."""
        return "{0} {1}".format(self.first_name, self.last_name)
