"""stat_analysis.models.statistics.py

"""
from django.db import models

from .report import Report


class JobReportResult(models.Model):
    """Model to store analysis results for the Jobs.

    `Job` model is defined in `execution` app.
    """
    report = models.OneToOneField(Report, on_delete=models.CASCADE)

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
    

class OrderReportResult(models.Model):
    """Model to store analysis results for the customer Orders.

    Note: `Order` model should be defined in Task 1.
    """
    report = models.OneToOneField(Report, on_delete=models.CASCADE)

    # Example data fields of what the order report may contain.
    total_orders = models.IntegerField()
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2)
