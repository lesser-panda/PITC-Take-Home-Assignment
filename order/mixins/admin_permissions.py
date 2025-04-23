from registrar import models as registrar_models


class OrderPermissionMixin:
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser or getattr(request.user, 'role', None) == 'admin':
            return qs

        if getattr(request.user, 'role', None) == 'account_manager':
            customer_ids = registrar_models.CustomerAccountManager.objects.filter(
                account_manager__user=request.user
            ).values_list('customer_id', flat=True)

            return qs.filter(customer_id__in=customer_ids)

        return qs.none()
    
    def get_form(self, request, obj=None, **kwargs):
        """Account managers can only create customers."""
        form = super().get_form(request, obj, **kwargs)
        if obj is None:
            # creating new user
            if request.user.role not in ["admin"] and not request.user.is_superuser:
                form.base_fields['role'].initial = 'customer'
                form.base_fields['role'].choices = [('customer', 'Customer')]
        return form
    
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or getattr(request.user, 'role', None) in ['account_manager', 'admin']
    
    def has_module_permission(self, request, obj=None):
        return request.user.is_superuser or getattr(request.user, 'role', None) in ['account_manager', 'admin']
    
    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser or getattr(request.user, 'role', None) == 'admin'
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or getattr(request.user, 'role', None) == 'admin'

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or getattr(request.user, 'role', None) == 'admin'


class OrderItemPermissionMixin:
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser or getattr(request.user, 'role', None) == 'admin':
            return qs

        if getattr(request.user, 'role', None) == 'account_manager':
            customer_ids = registrar_models.CustomerAccountManager.objects.filter(
                account_manager__user=request.user
            ).values_list('customer_id', flat=True)

            return qs.filter(order__customer_id__in=customer_ids)

        return qs.none()
    
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or getattr(request.user, 'role', None) in ['account_manager', 'admin']
    
    def has_module_permission(self, request, obj=None):
        return request.user.is_superuser or getattr(request.user, 'role', None) in ['account_manager', 'admin']
    
    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser or getattr(request.user, 'role', None) == 'admin'
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or getattr(request.user, 'role', None) == 'admin'

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or getattr(request.user, 'role', None) == 'admin'
    

class ProductAndServicePermissionMixin:
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser or getattr(request.user, 'role', None) == 'admin':
            return qs
        elif getattr(request.user, 'role', None) == 'account_manager':
            service_provider_ids = registrar_models.AccountManagerServiceProvider.objects.filter(
                account_manager__user=request.user
            ).values_list('service_provider_id', flat=True)
            return qs.filter(service_provider_id__in=service_provider_ids)
        elif getattr(request.user, 'role', None) == 'service_provider':
            return qs.filter(service_provider_id=request.user.service_provider_profile.id)
        else:
            return qs.none()
        
    def get_form(self, request, obj=None, **kwargs):
        """Service Providers can only create products for themselves
           while Account Managers can only create products for their service providers.
        """
        form = super().get_form(request, obj, **kwargs)
        if obj is None:
            # creating new product/service
            if request.user.role in ["service_provider"]:
                # service provider can only create products for themselves
                form.base_fields['service_provider'].initial = request.user.service_provider_profile
                form.base_fields['service_provider'].disabled = True
            elif request.user.role in ["account_manager"]:
                # account manager can only create products for their service providers
                service_provider_ids = registrar_models.AccountManagerServiceProvider.objects.filter(
                    account_manager__user=request.user
                ).values_list('service_provider_id', flat=True)
                form.base_fields['service_provider'].queryset = registrar_models.ServiceProviderProfile.objects.filter(
                    id__in=service_provider_ids
                )
        return form
        
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or getattr(request.user, 'role', None) in ['account_manager', 'admin', 'service_provider']
    
    def has_module_permission(self, request, obj=None):
        return request.user.is_superuser or getattr(request.user, 'role', None) in ['account_manager', 'admin', 'service_provider']

    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser or getattr(request.user, 'role', None) in ['account_manager', 'admin', 'service_provider']
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or getattr(request.user, 'role', None) in ['account_manager', 'admin', 'service_provider']

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or getattr(request.user, 'role', None) == 'admin'
