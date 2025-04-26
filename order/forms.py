from django import forms
from order import models as order_models
from registrar import models as registrar_models


class CustomerOrderForm(forms.ModelForm):
    """
    Form for customers to create an order. 
    Make sure that the user can only select
    account managers that are associated with their profile.
    """
    class Meta:
        model = order_models.Order
        fields = [
            'account_manager',
            'description',
        ]

    def __init__(self, *args, **kwargs):
        customer = kwargs.pop('customer', None)
        account_manager_ids = registrar_models.CustomerAccountManager.objects.filter(
            customer=customer
        ).values_list('account_manager__user_id', flat=True)
        super().__init__(*args, **kwargs)
        self.fields['account_manager'].queryset = registrar_models.AccountManagerProfile.objects.filter(
            user__id__in=account_manager_ids
        )
