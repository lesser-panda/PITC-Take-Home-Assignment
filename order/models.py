from django.db import models

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
    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    service_provider = models.ForeignKey(
        registrar_models.ServiceProviderProfile,
        on_delete=models.CASCADE,
        related_name="products",
    )


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
    service_provider = models.ForeignKey(
        registrar_models.ServiceProviderProfile,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"ODR {self.id} - CUST: {self.customer.user.email} - SP: {self.service_provider.user.email}"
    

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

    def __str__(self):
        return f"ODR {self.order.id} - {self.product.name} x {self.quantity}"
