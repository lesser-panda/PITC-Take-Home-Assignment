"""stat_analysis.models.report.py

"""
from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model


user_model = get_user_model()


class Report(models.Model):
    # metadata
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        user_model,
        on_delete=models.SET_NULL,
        related_name='created_reports',
        null=True,
        blank=True,
    )

    # Report settings 
    quarter_from = models.CharField(max_length=2)  # Q1, Q2, Q3, Q4
    year_from = models.IntegerField()
    quarter_to = models.CharField(max_length=2)  # Q1, Q2, Q3, Q4
    year_to = models.IntegerField()

    pdf_report = models.FileField(
        upload_to='reports_pdf/',
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf']),
        ],
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.title} ({self.year_from}{self.quarter_from} - {self.year_to}{self.quarter_to})"
    
    def save(self, *args, **kwargs):
        # import here to avoid circular import issues
        from stat_analysis.stat_utils import (
            calculate_order_stats,
            calculate_job_stats,
            calculate_user_stats,
        )
        """
        Run statistics calculation on creating or saaving a Report for
            - JobReportResult
            - OrderReportResult
            ...
            ... more to be implemented
        """
        super().save(*args, **kwargs)
        
        calculate_job_stats(
            quarter_from=self.quarter_from,
            year_from=self.year_from,
            quarter_to=self.quarter_to,
            year_to=self.year_to,
        )
        calculate_order_stats(
            quarter_from=self.quarter_from,
            year_from=self.year_from,
            quarter_to=self.quarter_to,
            year_to=self.year_to,
        )
        calculate_user_stats(
            quarter_from=self.quarter_from,
            year_from=self.year_from,
            quarter_to=self.quarter_to,
            year_to=self.year_to,
        )
