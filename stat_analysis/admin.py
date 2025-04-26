from django.contrib import admin
from stat_analysis import models as stat_analysis_models


admin.site.register([
    stat_analysis_models.Report
])


@admin.register(stat_analysis_models.JobReportResult)
class JobReportResultAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'report__title',
        'service_provider',
        'total_jobs',
        'average_completion_time_regular',
        'average_completion_time_wafer_run',
        'jobs_created',
        'jobs_active',
        'jobs_completed',
        'report__created_at',
    ]
    list_filter = [
        'service_provider',
        'report__title',
    ]
    ordering = ['-id']


@admin.register(stat_analysis_models.OrderReportResult)
class OrderReportResultAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'report__title',
        'total_orders',
        'total_amount',
        'average_amount',
        'order_new',
        'order_pending',
        'order_completed',
        'order_closed',
        'report__created_at',
    ]
    list_filter = [
        'report__title',
    ]
    ordering = ['-id']


@admin.register(stat_analysis_models.UserReportResult)
class UserReportResultAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'report__title',
        'total_users',
        'total_customers',
        'total_account_managers',
        'total_service_providers',
        'average_orders_per_user',
        'average_customers_per_account_manager',
        'report__created_at',
    ]
    list_filter = [
        'report__title',
    ]
    ordering = ['-id']
