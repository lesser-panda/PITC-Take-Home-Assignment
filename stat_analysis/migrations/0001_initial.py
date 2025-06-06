# Generated by Django 5.2 on 2025-04-24 16:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('quarter_from', models.CharField(max_length=2)),
                ('year_from', models.IntegerField()),
                ('quarter_to', models.CharField(max_length=2)),
                ('year_to', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='OrderReportResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_orders', models.IntegerField()),
                ('total_revenue', models.DecimalField(decimal_places=2, max_digits=10)),
                ('average_order_value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('report', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='stat_analysis.report')),
            ],
        ),
        migrations.CreateModel(
            name='JobReportResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_jobs', models.IntegerField()),
                ('average_completion_time_regular', models.FloatField(blank=True, help_text='Average completion time for regular jobs in days.', null=True)),
                ('average_completion_time_wafer_run', models.FloatField(blank=True, help_text='Average completion time for wafer run jobs in days.', null=True)),
                ('jobs_created', models.IntegerField(default=0, help_text="Number of jobs with 'Created' state in the given period.")),
                ('jobs_active', models.IntegerField(default=0, help_text="Number of jobs with 'Active' state in the given period.")),
                ('jobs_completed', models.IntegerField(default=0, help_text="Number of jobs with 'Completed' state in the given period.")),
                ('report', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='stat_analysis.report')),
            ],
        ),
    ]
