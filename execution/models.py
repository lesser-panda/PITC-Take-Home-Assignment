"""execution.models.py

This script defines the Job model which is used to track
the execution progress of customer orders.
"""
from django.db import models


class Job(models.Model):

    JOB_TYPE_CHOICES = [
        ('regular', 'Regular'),
        ('wafer_run', 'Wafer Run'),
    ]

    job_name = models.CharField(max_length=200)

    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)

    starting_date = models.DateTimeField()
    end_date = models.DateTimeField()
    completion_time = models.FloatField(help_text="Time in days which were spent to complete the job.")

    def save(self, *args, **kwargs):
        created = not self.id
        super().save(*args, **kwargs)
        if created:
            # Create initial job status
            JobState.objects.create(job=self, state_date=self.starting_date, state='created')

    def __str__(self):
        return self.job_name
    

class JobState(models.Model):
    """
    Keep track of the job state changes so that when we create a report
    retrospectively, we can still accurately report the statistics for 
    jobs during a given time period in the past.
    """

    STATE_CHOICES = [
        ('created', 'Created'),
        ('active', 'Active'),
        ('completed', 'Completed'),
    ]

    state_date = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=20, choices=STATE_CHOICES)

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='job_states',
    )

    def __str__(self):
        return f"Job:#{self.job.id} changed to {self.state} on {self.state_date}"
