from django.db.models.signals import post_save
from django.dispatch import receiver
from registrar.models import (
    User,
    CustomerProfile,
    AccountManagerProfile,
    ServiceProviderProfile,
)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create a user profile when a new user is created.
    """
    if created:
        if instance.role == "customer":
            CustomerProfile.objects.create(user=instance)
        elif instance.role == "account_manager":
            AccountManagerProfile.objects.create(user=instance)
        elif instance.role == "service_provider":
            ServiceProviderProfile.objects.create(user=instance)
