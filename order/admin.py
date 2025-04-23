from django.contrib import admin
from order import models as order_models
from order.mixins.admin_permissions import (
    OrderPermissionMixin,
    OrderItemPermissionMixin,
    ProductAndServicePermissionMixin,
)


@admin.register(order_models.ProductAndService)
class ProductAndServiceAdmin(ProductAndServicePermissionMixin, admin.ModelAdmin):
    list_display = [
        'id', 
        'name',
        'type',
        'price',
        'service_provider__user__email',
    ]
    ordering = ['-created_at']


@admin.register(order_models.Order)
class OrderAdmin(OrderPermissionMixin, admin.ModelAdmin):
    list_display = [
        'id', 
        'customer__user__email',
        'account_manager__user__email',
        'service_provider__user__email', 
        'created_at',
    ]
    ordering = ['-created_at']


@admin.register(order_models.OrderItem)
class OrderItemAdmin(OrderItemPermissionMixin, admin.ModelAdmin):
    list_display = [
        'id', 
        'order__id',
        'product__name',
        'product__type',
        'quantity',
        'order__customer__user__email',
        'order__account_manager__user__email',
        'order__service_provider__user__email',
    ]
    ordering = ['-created_at']
