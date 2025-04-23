from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from registrar import models as registrar_models
from registrar.mixins.admin_permissions import UserProfilePermissionMixin


@admin.register(registrar_models.User)
class CustomUserAdmin(UserProfilePermissionMixin, UserAdmin):
    model = registrar_models.User

    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {
            "fields": (
                "role",
                "address",
                "company",
                "website",
                "phone",
                "bio",
            )
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional info", {
            "fields": (
                "role",
            )
        }),
    )

    list_display = ("email", "username", "role", "is_staff", "is_active", "is_superuser")
    list_filter = ("role", "is_staff", "is_superuser")
    search_fields = ("email", "username", "first_name", "last_name")

    def save_model(self, request, obj, form, change):
        manager_created_new_customer = (not change and request.user.role == "account_manager" and obj.role == "customer")
        super().save_model(request, obj, form, change)
        if manager_created_new_customer:
            customer_profile, _ = registrar_models.CustomerProfile.objects.get_or_create(user=obj)
            registrar_models.CustomerAccountManager.objects.get_or_create(
                customer=customer_profile,
                account_manager=request.user.account_manager_profile,
            )


admin.site.register([
    registrar_models.CustomerProfile,
    registrar_models.AccountManagerProfile,
    registrar_models.ServiceProviderProfile,
    registrar_models.AccountManagerServiceProvider,
    registrar_models.CustomerAccountManager,
])


admin.site.site_header = "JePPIX Admin Portal"
admin.site.site_title = "JePPIX Admin Portal"
admin.site.index_title = "Welcome to JePPIX Admin Portal"
