from django.test import TestCase
from django.contrib.auth import get_user_model
import datetime

from registrar.models import (
    ServiceProviderProfile,
    CustomerProfile,
    AccountManagerProfile,
    AccountManagerServiceProvider,
    CustomerAccountManager,
)
from execution.models import Job
from stat_analysis import stat_utils


User = get_user_model()


class StatUtilsTests(TestCase):

    @classmethod
    def setUpTestData(self):
        self.user_service_provider_1 = User.objects.create_user(
            username='service_provider_1',
            email="service_1@tue.nl",
            password="password123",
            role='service_provider',
            is_active=True,
            is_staff=True,
            first_name="Joey",
            last_name="Tribiani",
        )
        self.user_service_provider_2 = User.objects.create_user(
            username='service_provider_2',
            email="service_2@tue.nl",
            password="password123",
            role='service_provider',
            is_active=True,
            is_staff=True,
            first_name="Chandler",
            last_name="Bing",
        )
        self.user_customer_1 = User.objects.create_user(
            username='customer_1',
            email="customer_1@tue.nl",
            password="password123",
            role='customer',
            is_active=True,
            first_name="Phoebe",
            last_name="Buffay",
        )
        self.user_customer_2 = User.objects.create_user(
            username='customer_2',
            email="customer_2@tue.nl",
            password="password123",
            role='customer',
            is_active=True,
            first_name="Ross",
            last_name="Geller",
        )
        self.user_account_manager_1 = User.objects.create_user(
            username='account_manager_1',
            email="account_manager_1@tue.nl",
            password="password123",
            role='account_manager',
            is_active=True,
            is_staff=True,
            first_name="Monica",
            last_name="Geller",
        )
        self.user_account_manager_2 = User.objects.create_user(
            username='account_manager_2',
            email="account_manager_2@tue.nl",
            password="password123",
            role='account_manager',
            is_active=True,
            is_staff=True,
            first_name="Rachel",
            last_name="Green",
        )
        self.service_provider_1 = ServiceProviderProfile.objects.filter(user=self.user_service_provider_1).first()
        self.service_provider_2 = ServiceProviderProfile.objects.filter(user=self.user_service_provider_2).first()
        self.customer_1 = CustomerProfile.objects.filter(user=self.user_customer_1).first()
        self.customer_2 = CustomerProfile.objects.filter(user=self.user_customer_2).first()
        self.account_manager_1 = AccountManagerProfile.objects.filter(user=self.user_account_manager_1).first()
        self.account_manager_2 = AccountManagerProfile.objects.filter(user=self.user_account_manager_2).first()
        self.customer_1_account_manager_1_relationship = CustomerAccountManager.objects.create(
            customer=self.customer_1,
            account_manager=self.account_manager_1,
        )
        self.customer_2_account_manager_1_relationship = CustomerAccountManager.objects.create(
            customer=self.customer_2,
            account_manager=self.account_manager_1,
        )
        self.account_manager_1_service_provider_1_relationship = AccountManagerServiceProvider.objects.create(
            account_manager=self.account_manager_1,
            service_provider=self.service_provider_1,
        )
        self.account_manager_1_service_provider_2_relationship = AccountManagerServiceProvider.objects.create(
            account_manager=self.account_manager_1,
            service_provider=self.service_provider_2,
        )

        self.assertIsNotNone(
            self.service_provider_1 and self.user_customer_1 and self.user_account_manager_1, 
            "User profile should be created automatically."
        )

        self.job_1 = Job.objects.create(
            job_name="Job 1",
            job_type="regular",
            service_provider=self.service_provider_1,
            completion_time=40,
        )
        self.job_1.job_states.all().delete()
        self.job_1.job_states.create(
            job=self.job_1,
            state_date=datetime.datetime(2024, 10, 26),
            state='created',
        )
        self.job_1.job_states.create(
            job=self.job_1,
            state_date=datetime.datetime(2024, 10, 28),
            state='active',
        )
        self.job_1.job_states.create(
            job=self.job_1,
            state_date=datetime.datetime(2024, 12, 26),
            state='completed',
        )

        self.job_2 = Job.objects.create(
            job_name="Job 2",
            job_type="regular",
            service_provider=self.service_provider_1,
            completion_time=20,
        )
        self.job_2.job_states.all().delete()
        self.job_2.job_states.create(
            job=self.job_2,
            state_date=datetime.datetime(2024, 10, 26),
            state='created',
        )
        self.job_2.job_states.create(
            job=self.job_2,
            state_date=datetime.datetime(2024, 10, 28),
            state='active',
        )
        self.job_2.job_states.create(
            job=self.job_2,
            state_date=datetime.datetime(2024, 11, 26),
            state='completed',
        )

        self.job_3 = Job.objects.create(
            job_name="Job 3",
            job_type="regular",
            service_provider=self.service_provider_2,
            # never completed
        )
        self.job_3.job_states.all().delete()
        self.job_3.job_states.create(
            job=self.job_3,
            state_date=datetime.datetime(2024, 10, 26),
            state='created',
        )
        self.job_3.job_states.create(
            job=self.job_3,
            state_date=datetime.datetime(2024, 10, 26),
            state='active',
        )

        self.job_4 = Job.objects.create(
            job_name="Job 3",
            job_type="wafer_run",
            service_provider=self.service_provider_1,
            # never completed
        )
        self.job_4.job_states.all().delete()
        self.job_4.job_states.create(
            job=self.job_4,
            state_date=datetime.datetime(2024, 11, 26),
            state='created',
        )
        self.job_4.job_states.create(
            job=self.job_4,
            state_date=datetime.datetime(2024, 11, 26),
            state='active',
        )

        self.order_1 = self.job_1.orders.create(
            customer=self.customer_1,
            account_manager=self.account_manager_1,
            description="Order 1 description",
            amount=100.00,
        )
        self.order_2 = self.job_1.orders.create(
            customer=self.customer_2,
            account_manager=self.account_manager_1,
            description="Order 2 description",
            amount=200.00,
        )
        self.order_3 = self.job_2.orders.create(
            customer=self.customer_1,
            account_manager=self.account_manager_1,
            description="Order 2 description",
            amount=200.00,
        )

    def test_get_average_completion_time(self):
        """Test the average completion time for regular jobs."""
        avg_completion_time_sp_1 = stat_utils.get_average_completion_time(
            job_type='regular',
            start_date=datetime.date(2024, 9, 1),
            end_date=datetime.date(2024, 12, 31),
            service_provider=self.service_provider_1,
        )
        self.assertAlmostEqual(avg_completion_time_sp_1, 30.0, places=2)

    def test_get_average_completion_time_no_jobs(self):
        """Test the average completion time when no jobs are present in the given job type"""
        avg_completion_time_sp_1 = stat_utils.get_average_completion_time(
            job_type='wafer_run',
            start_date=datetime.date(2024, 9, 1),
            end_date=datetime.date(2024, 12, 31),
            service_provider=self.service_provider_1,
        )
        self.assertEqual(avg_completion_time_sp_1, 0.0)

    def test_get_average_completion_time_no_completed_jobs(self):
        """Test the average completion time when no jobs have a completion time"""
        avg_completion_time_sp_2 = stat_utils.get_average_completion_time(
            job_type='regular',
            start_date=datetime.date(2024, 9, 1),
            end_date=datetime.date(2024, 12, 31),
            service_provider=self.service_provider_2,
        )
        self.assertEqual(avg_completion_time_sp_2, 0.0)

    def test_job_state_count(self):
        job_state_count = stat_utils.get_job_state_count(
            start_date=datetime.date(2024, 10, 1),
            end_date=datetime.date(2024, 12, 31),
            service_provider=self.service_provider_1,
        )
        self.assertEqual(job_state_count['created'], 0)
        self.assertEqual(job_state_count['active'], 1)
        self.assertEqual(job_state_count['completed'], 2)

# extend the unit test cases for actual production environment.
# not gonna spend all my time on this for now :-)
# also add integration tests for the entire Report generation process.
