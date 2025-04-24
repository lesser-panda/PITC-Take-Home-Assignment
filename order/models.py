from django.db import models
from django.urls import reverse

from registrar import models as registrar_models


class TimeStampBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class ProductAndService(TimeStampBaseModel):
    TYPE_CHOICES = (
        ("product", "Product"),
        ("service", "Service"),
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="product")
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    service_provider = models.ForeignKey(
        registrar_models.ServiceProviderProfile,
        on_delete=models.CASCADE,
        related_name="products",
    )

    def __str__(self):
        return f"{self.name} - {self.type} - {self.service_provider.user.email}"


class Order(TimeStampBaseModel):
    STATUS_CHOICES = (
        ("new", "New"),
        ("pending", "Pending"),
        ("closed", "Closed"),
        ("completed", "Completed"),
    )

    customer = models.ForeignKey(
        registrar_models.CustomerProfile,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    account_manager = models.ForeignKey(
        registrar_models.AccountManagerProfile,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"ODR {self.id} - CUST: {self.customer.user.email} - AM: {self.account_manager.user.email}"
    
    def save(self, *args, **kwargs):
        """
        Users can only create orders with account managers that are connected to their customer profile.
        """
        connected_account_manager_ids = registrar_models.CustomerAccountManager.objects.filter(
            customer=self.customer
        ).values_list("account_manager_id", flat=True)
        if self.account_manager.id not in connected_account_manager_ids:
            raise ValueError("You cannot create orders with this account manager.")
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("customer_order_detail", kwargs={"order_id": self.id})


class OrderItem(TimeStampBaseModel):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(
        ProductAndService,
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField(blank=False, null=False)

    def save(self, *args, **kwargs):
        """
        Prevent users from adding products/services provided by service providers
        that are not managed by their account manager.
        """
        allowed_service_provider_ids = registrar_models.AccountManagerServiceProvider.objects.filter(
            account_manager__user=self.order.account_manager.user
        ).values_list("service_provider_id", flat=True)

        if self.product.service_provider.id not in allowed_service_provider_ids:
            raise ValueError("You are not allowed to add this product to the order. Please contact your Account Manager")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"ODR {self.order.id} - {self.product.name} x {self.quantity}"
