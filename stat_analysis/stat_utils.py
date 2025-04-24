from collections import defaultdict
import datetime

from django.db.models import OuterRef, Subquery, Max
from django.apps import apps


job_model = apps.get_model("execution", "Job")
job_states_model = apps.get_model("execution", "JobState")
job_stats_model = apps.get_model("stat_analysis", "JobReportResult")
order_model = apps.get_model("order", "Order")
order_stats_model = apps.get_model("stat_analysis", "OrderReportResult")
report_model = apps.get_model("stat_analysis", "Report")


def get_quarter_dates(quarter, year):
    if quarter == 'Q1':
        start_date = datetime.date(year, 1, 1)
        end_date = datetime.date(year, 3, 31)
    elif quarter == 'Q2':
        start_date = datetime.date(year, 4, 1)
        end_date = datetime.date(year, 6, 30)
    elif quarter == 'Q3':
        start_date = datetime.date(year, 7, 1)
        end_date = datetime.date(year, 9, 30)
    elif quarter == 'Q4':
        start_date = datetime.date(year, 10, 1)
        end_date = datetime.date(year, 12, 31)
    else:
        raise ValueError("Invalid quarter. Please use 'Q1', 'Q2', 'Q3', or 'Q4'.")
    return start_date, end_date


def get_average_completion_time(job_type, start_date, end_date):
    """Calculate average completion time for a specific job type."""
    job_types = job_model.JOB_TYPE_CHOICES
    if job_type not in dict(job_types):
        raise ValueError(f"Invalid job type. Please use one of {dict(job_types).keys()}.")
    jobs = job_model.objects.filter(
        job_type=job_type,
        starting_date__gte=start_date,
        end_date__lte=end_date
    )
    if jobs.exists():
        total_completion_time = sum(job.completion_time for job in jobs)
        average_completion_time = total_completion_time / jobs.count()
    else:
        average_completion_time = 0.0
    return average_completion_time


def get_job_state_count(start_date, end_date):
    """
    Since each job can have multiple states, we need to get the
    latest state for each job within the given time range to count
    the number of jobs in each state correctly.
    """
    # Get the latest state_date per job within the time range
    latest_state_dates = job_states_model.objects.filter(
        state_date__gte=start_date,
        state_date__lte=end_date,
        job=OuterRef('job')
    ).order_by('-state_date')

    latest_states = job_states_model.objects.filter(
        pk__in=Subquery(
            job_states_model.objects.filter(
                state_date__gte=start_date,
                state_date__lte=end_date
            )
            .values('job')
            .annotate(latest_id=Max('id'))
            .values('latest_id')
        )
    )

    job_states_count = defaultdict(int)
    for job_state in latest_states:
        job_states_count[job_state.state] += 1

    return job_states_count


def calculate_job_stats(quarter_from, year_from, quarter_to, year_to):
    """Calculate statistics for Job model for a given period."""

    start_date_from, end_date_from = get_quarter_dates(quarter_from, year_from)
    start_date_to, end_date_to = get_quarter_dates(quarter_to, year_to)

    start_date = min(start_date_from, start_date_to)
    end_date = max(end_date_from, end_date_to)

    total_jobs = job_model.objects.filter(
        starting_date__gte=start_date,
        end_date__lte=end_date
    ).count()
    average_completion_time_regular = get_average_completion_time(
        'regular', start_date, end_date
    )
    average_completion_time_wafer_run = get_average_completion_time(
        'wafer_run', start_date, end_date
    )

    job_states_count = get_job_state_count(start_date, end_date)
    jobs_created = job_states_count.get('created', 0)
    jobs_active = job_states_count.get('active', 0)
    jobs_completed = job_states_count.get('completed', 0)

    report, created = report_model.objects.get_or_create(
        quarter_from=quarter_from,
        year_from=year_from,
        quarter_to=quarter_to,
        year_to=year_to,
        defaults={
            'title': 'Job Report',
            'created_at': datetime.datetime.now(),
            'created_by': 'system',
        }
    )

    job_stats, created = job_stats_model.objects.get_or_create(
        report=report,
        defaults={
            'total_jobs': total_jobs,
            'average_completion_time_regular': average_completion_time_regular,
            'average_completion_time_wafer_run': average_completion_time_wafer_run,
            'jobs_created': jobs_created,
            'jobs_active': jobs_active,
            'jobs_completed': jobs_completed,
        }
    )

    if not created:
        job_stats.total_jobs = total_jobs
        job_stats.save()

    return job_stats


def calculate_order_stats(quarter_from, year_from, quarter_to, year_to):
    """Calculate statistics for Order model for a given period."""
    start_date_from, end_date_from = get_quarter_dates(quarter_from, year_from)
    start_date_to, end_date_to = get_quarter_dates(quarter_to, year_to)

    start_date = min(start_date_from, start_date_to)
    end_date = max(end_date_from, end_date_to)

