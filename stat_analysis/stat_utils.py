from collections import defaultdict
import datetime

from django.db.models import Subquery, Max, OuterRef
from django.apps import apps
from django.contrib.auth import get_user_model


job_model = apps.get_model("execution", "Job")
job_states_model = apps.get_model("execution", "JobState")
job_stats_model = apps.get_model("stat_analysis", "JobReportResult")
order_model = apps.get_model("order", "Order")
order_states_model = apps.get_model("order", "OrderState")
order_stats_model = apps.get_model("stat_analysis", "OrderReportResult")
report_model = apps.get_model("stat_analysis", "Report")
service_provider_model = apps.get_model("registrar", "ServiceProviderProfile")
user_model = get_user_model("stat_analysis", "UserReportResult")


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


def get_average_completion_time(job_type, start_date, end_date, service_provider=None):
    """Calculate average completion time for a specific job type."""
    job_types = job_model.JOB_TYPE_CHOICES
    if job_type not in dict(job_types):
        raise ValueError(f"Invalid job type. Please use one of {dict(job_types).keys()}.")
    
    if service_provider:
        jobs = job_model.objects.filter(
            job_type=job_type,
            completion_time__isnull=False,
            service_provider=service_provider,
        ).exclude(completion_time=0)
    else:
        jobs = job_model.objects.filter(
            job_type=job_type,
            completion_time__isnull=False,
        ).exclude(completion_time=0)

    jobs = [
        job for job in jobs
        if job.starting_date.date() and job.end_date and
        job.starting_date.date() >= start_date and job.end_date.date() <= end_date
    ]

    if jobs:
        total_completion_time = sum(job.completion_time for job in jobs)
        average_completion_time = total_completion_time / len(jobs)
    else:
        average_completion_time = 0.0
    return average_completion_time


def get_job_state_count(start_date, end_date, service_provider=None):
    """
    Since each job can have multiple states, we need to get the
    latest state for each job within the given time range to count
    the number of jobs in each state correctly.
    """
    if service_provider:
        latest_states = job_states_model.objects.filter(
            pk__in=Subquery(
                job_states_model.objects.filter(
                    state_date__gte=start_date,
                    state_date__lte=end_date,
                    job__service_provider=service_provider,
                )
                .values('job')
                .annotate(latest_id=Max('id'))
                .values('latest_id')
            )
        )
    else:
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

    jobs = job_model.objects.prefetch_related('job_states')
    service_providers = service_provider_model.objects.all()
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

    for service_provider in service_providers:
        current_provider_jobs = jobs.filter(service_provider=service_provider).all()
        current_provider_jobs = [
            job for job in current_provider_jobs
            if job.starting_date.date() and start_date <= job.starting_date.date() <= end_date
        ]

        total_jobs = len(current_provider_jobs)

        average_completion_time_regular = get_average_completion_time(
            'regular', start_date, end_date, service_provider
        )
        average_completion_time_wafer_run = get_average_completion_time(
            'wafer_run', start_date, end_date, service_provider
        )

        job_states_count = get_job_state_count(start_date, end_date, service_provider)
        jobs_created = job_states_count.get('created', 0)
        jobs_active = job_states_count.get('active', 0)
        jobs_completed = job_states_count.get('completed', 0)

        job_stats, created = job_stats_model.objects.update_or_create(
            report=report,
            service_provider=service_provider,
            defaults={
                'total_jobs': total_jobs,
                'average_completion_time_regular': average_completion_time_regular,
                'average_completion_time_wafer_run': average_completion_time_wafer_run,
                'jobs_created': jobs_created,
                'jobs_active': jobs_active,
                'jobs_completed': jobs_completed,
            }
        )


def get_order_state_count(start_date, end_date):
    """
    Since each order can have multiple states, we need to get the
    latest state for each order within the given time range to count
    the number of jobs in each state correctly.
    """
    latest_states = order_states_model.objects.filter(
        pk__in=Subquery(
            order_states_model.objects.filter(
                state_date__gte=start_date,
                state_date__lte=end_date
            )
            .values('order')
            .annotate(latest_id=Max('id'))
            .values('latest_id')
        )
    )

    order_states_count = defaultdict(int)
    for order_state in latest_states:
        order_states_count[order_state.state] += 1

    return order_states_count


def calculate_order_stats(quarter_from, year_from, quarter_to, year_to):
    """Calculate statistics for Order model for a given period."""
    start_date_from, end_date_from = get_quarter_dates(quarter_from, year_from)
    start_date_to, end_date_to = get_quarter_dates(quarter_to, year_to)

    start_date = min(start_date_from, start_date_to)
    end_date = max(end_date_from, end_date_to)
    
    orders = order_model.objects.prefetch_related('order_states').all()
    orders = [
        order for order in orders
        if order.starting_date.date() and start_date <= order.starting_date.date() <= end_date
    ]
    total_orders = len(orders)

    total_amount = sum(order.amount for order in orders if order.amount is not None)

    average_amount = total_amount / total_orders if total_orders > 0 else 0.0
    order_states_count = get_order_state_count(start_date, end_date)

    order_new = order_states_count.get("new", 0)
    order_pending = order_states_count.get("pending", 0)
    order_closed = order_states_count.get("closed", 0)
    order_completed = order_states_count.get("completed", 0)

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

    order_stats, created = order_stats_model.objects.update_or_create(
        report=report,
        defaults={
            'total_orders': total_orders,
            'total_amount': total_amount,
            'average_amount': average_amount,
            'order_new': order_new,
            'order_pending': order_pending,
            'order_closed': order_closed,
            'order_completed': order_completed,
        }
    )


def calculate_user_stats(quarter_from, year_from, quarter_to, year_to):
    """Calculate statistics for User model for a given period."""
    start_date_from, end_date_from = get_quarter_dates(quarter_from, year_from)
    start_date_to, end_date_to = get_quarter_dates(quarter_to, year_to)

    start_date = min(start_date_from, start_date_to)
    end_date = max(end_date_from, end_date_to)

    all_users = user_model.objects.filter(
        date_joined__gte=start_date,
        date_joined__lte=end_date
    )
    user_count = all_users.count()
    customer_count = all_users.filter(role=user_model.ROLE_CHOICES.customer).count()
    account_manager_count = all_users.filter(role=user_model.ROLE_CHOICES.account_manager).count()
    service_provider_count = all_users.filter(role=user_model.ROLE_CHOICES.service_provider).count()

    order_first_state_subquery = order_states_model.objects.filter(
        order=OuterRef('pk')
    ).order_by('state_date').values('state_date')[:1]

    order_created_during_date_range = order_model.objects.annotate(
        creation_date=Subquery(order_first_state_subquery)
    ).filter(
        creation_date__gte=start_date,
        creation_date__lte=end_date,
    )

    total_orders = order_created_during_date_range.count()
    average_orders_per_user = total_orders / user_count if user_count > 0 else 0.0
    average_customers_per_account_manager = customer_count / account_manager_count if account_manager_count > 0 else 0.0

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

    user_stats, created = user_model.objects.update_or_create(
        report=report,
        defaults={
            "total_users": user_count,
            "total_customers": customer_count,
            "total_account_managers": account_manager_count,
            "total_service_providers": service_provider_count,
            "average_orders_per_user": average_orders_per_user,
            "average_customers_per_account_manager": average_customers_per_account_manager,
        },
    )
