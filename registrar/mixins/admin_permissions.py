import registrar.models as registrar_models


class UserProfilePermissionMixin:
    """
    Custom permission mixin for the UserProfile model in the admin interface.
    """

    def get_queryset(self, request):
        """Account managers can only see their OWN customers."""
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.role == 'admin':
            return qs
        elif request.user.role == 'account_manager':
            customer_ids = registrar_models.CustomerAccountManager.objects.filter(
                account_manager__user=request.user
            ).values_list('customer__user_id', flat=True)
            query = qs.filter(role='customer', id__in=customer_ids)
            return query
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
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('role',)
        return self.readonly_fields

    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser \
            or getattr(request.user, 'role', None) in ['account_manager', 'admin']
    
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser \
            or getattr(request.user, 'role', None) in ['account_manager', 'admin']

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser \
            or getattr(request.user, 'role', None) in ['account_manager', 'admin']
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser \
            or getattr(request.user, 'role', None) in ['account_manager', 'admin']
    
    def has_module_permission(self, request, obj=None):
        return request.user.is_superuser \
            or getattr(request.user, 'role', None) in ['account_manager', 'admin']
    

class CustomerAccountManagerPermissionMixin:
    """
    Custom permission mixin for the CustomerAccountManager model in the admin interface.
    """

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.role == 'admin':
            return qs
        elif request.user.role == 'account_manager':
            customer_ids = registrar_models.CustomerAccountManager.objects.filter(
                account_manager__user=request.user
            ).values_list('customer_id', flat=True)
            return qs.filter(customer_id__in=customer_ids)
        return qs.none()
    