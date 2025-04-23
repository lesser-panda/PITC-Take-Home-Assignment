from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from registrar.models import AccountManagerServiceProvider, CustomerAccountManager


@receiver(post_save, sender=Order)
def create_relationships_on_order(sender, instance, created, **kwargs):
    if not created:
        return

    customer = instance.customer
    account_manager = instance.account_manager
    service_provider = instance.service_provider

    if not CustomerAccountManager.objects.filter(
        customer=customer,
        account_manager=account_manager
    ).exists():
        CustomerAccountManager.objects.create(
            customer=customer,
            account_manager=account_manager
        )

    if not AccountManagerServiceProvider.objects.filter(
        account_manager=account_manager,
        service_provider=service_provider
    ).exists():
        AccountManagerServiceProvider.objects.create(
            account_manager=account_manager,
            service_provider=service_provider
        )
