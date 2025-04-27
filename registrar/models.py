from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("account_manager", "Account Manager"),
        ("service_provider", "Service Provider"),
        ("customer", "Customer"),
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="admin",
    )
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    company = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.email} - {self.role}"

    def save(self, *args, **kwargs):
        created = not self.id
        super().save(*args, **kwargs)

        if created:
            if self.role == "customer":
                CustomerProfile.objects.create(user=self)
            elif self.role == "account_manager":
                AccountManagerProfile.objects.create(user=self)
            elif self.role == "service_provider":
                ServiceProviderProfile.objects.create(user=self)


class ServiceProviderProfile(TimeStampBaseModel):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'service_provider'},
        related_name='service_provider_profile'
    )

    def __str__(self):
        return f"{self.user.email}"


class AccountManagerProfile(TimeStampBaseModel):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'account_manager'},
        related_name='account_manager_profile'
    )

    service_providers = models.ManyToManyField(
        ServiceProviderProfile,
        limit_choices_to={'role': 'service_provider'},
        blank=True,
        through='AccountManagerServiceProvider',
        through_fields=('account_manager', 'service_provider'),
        related_name="account_managers",
    )

    def __str__(self):
        return f"{self.user.email}"


class CustomerProfile(TimeStampBaseModel):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'customer'},
        related_name='customer_profile',
    )

    account_managers = models.ManyToManyField(
        AccountManagerProfile,
        limit_choices_to={'role': 'account_manager'},
        blank=True,
        through_fields=('customer', 'account_manager'),
        through='CustomerAccountManager',
        related_name='customers',
    )

    def __str__(self):
        return f"{self.user.email}"


class AccountManagerServiceProvider(TimeStampBaseModel):
    """
    Relationship table to keep track of who 
    is the account manager for which service provider.
    When an account manager creates a service provider,
    the service provider is automatically linked to the account manager.
    An account manager can manage multiple service providers,
    but cannot create this relationship manually themselves as limited 
    by the Admin permission settings. 
    """

    account_manager = models.ForeignKey(AccountManagerProfile, on_delete=models.CASCADE)
    service_provider = models.ForeignKey(ServiceProviderProfile, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Relationship: Account Manager - Service Provider"
        verbose_name_plural = "Relationships: Account Manager - Service Provider"
        unique_together = ('account_manager', 'service_provider')

    def __str__(self):
        return f"AM: {self.account_manager.user.email} - SP: {self.service_provider.user.email}"
    

class CustomerAccountManager(TimeStampBaseModel):
    """
    Relationship table to keep track of who 
    is the account manager for which customer.
    An account manager can have multiple customers.
    When the customer is created by an account manager,
    the account manager is automatically linked to the customer.
    However, this relationship cannot be created manually by the account manager.
    A customer can have multiple account managers. This relationship
    can be created manually by the admin.
    """

    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    account_manager = models.ForeignKey(AccountManagerProfile, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Relationship: Account Manager - Customer"
        verbose_name_plural = "Relationships: Account Manager - Customer"
        unique_together = ('customer', 'account_manager')

    def __str__(self):
        return f"CUST: {self.customer.user.email} - AM: {self.account_manager.user.email}"
