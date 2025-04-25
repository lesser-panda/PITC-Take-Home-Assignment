"""stat_analysis.models.report.py

"""
from django.db import models


class Report(models.Model):
    # metadata
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = ...

    # Report settings 
    quarter_from = models.CharField(max_length=2)  # Q1, Q2, Q3, Q4
    year_from = models.IntegerField()
    quarter_to = models.CharField(max_length=2)  # Q1, Q2, Q3, Q4
    year_to = models.IntegerField()

    def __str__(self):
        return f"{self.title} ({self.year_from}{self.quarter_from} - {self.year_to}{self.quarter_to})"
    
    def save(self, *args, **kwargs):
        from stat_analysis.stat_utils import (
            calculate_order_stats,
            calculate_job_stats,
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
