"""stat_analysis.models.statistics.py

"""
from django.db import models

from stat_analysis.models import Report


class JobReportResult(models.Model):
    """Model to store analysis results for the Jobs

    `Job` model is defined in `execution` app.

    Changes:
        - Changed relationship to Report to OneToMany, and have
            separate JobReportResult for each Service Providers.
        - Added more fields for statistics as requested.
    """
    report = models.ForeignKey(
        Report, 
        on_delete=models.CASCADE,
        related_name='job_report_results',
    )

    service_provider = models.ForeignKey(
        'registrar.ServiceProviderProfile',
        on_delete=models.CASCADE,
        related_name='job_report_results',
    )

    total_jobs = models.IntegerField()

    average_completion_time_regular = models.FloatField(
        help_text="Average completion time for regular jobs in days.",
        null=True,
        blank=True,
    )
    average_completion_time_wafer_run = models.FloatField(
        help_text="Average completion time for wafer run jobs in days.",
        null=True,
        blank=True,
    )

    jobs_created = models.IntegerField(
        help_text="Number of jobs with 'Created' state in the given period.",
        default=0,
    )
    jobs_active = models.IntegerField(
        help_text="Number of jobs with 'Active' state in the given period.",
        default=0,
    )
    jobs_completed = models.IntegerField(
        help_text="Number of jobs with 'Completed' state in the given period.",
        default=0,
    )

    def __str__(self):
        return f"Job Report Result for {self.report.title} ({self.report.year_from}{self.report.quarter_from} - {self.report.year_to}{self.report.quarter_to})"
    

class OrderReportResult(models.Model):
    """Model to store analysis results for the customer Orders.

    Note: `Order` model should be defined in Task 1.
    """
    report = models.OneToOneField(Report, on_delete=models.CASCADE)

    total_orders = models.IntegerField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    average_amount = models.DecimalField(max_digits=12, decimal_places=2)
    order_new = models.IntegerField()
    order_pending = models.IntegerField()
    order_completed = models.IntegerField()
    order_closed = models.IntegerField()

    def __str__(self):
        return f"Order Report Result for {self.report.title} ({self.report.year_from}{self.report.quarter_from} - {self.report.year_to}{self.report.quarter_to})"


class UserReportResult(models.Model):
    """
    Model to store analysis results for the Users.
    """
    report = models.OneToOneField(Report, on_delete=models.CASCADE)

    total_users = models.IntegerField()
    total_customers = models.IntegerField()
    total_account_managers = models.IntegerField()
    total_service_providers = models.IntegerField()
    average_orders_per_user = models.FloatField()
    average_customers_per_account_manager = models.FloatField()

    def __str__(self):
        return f"User Report Result for {self.report.title} ({self.report.year_from}{self.report.quarter_from} - {self.report.year_to}{self.report.quarter_to})"
