# Generated by Django 5.2 on 2025-04-24 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('execution', '0002_remove_job_job_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jobstate',
            old_name='status_date',
            new_name='state_date',
        ),
        migrations.AddField(
            model_name='jobstate',
            name='state',
            field=models.CharField(choices=[('created', 'Created'), ('active', 'Active'), ('completed', 'Completed')], default='created', max_length=20),
            preserve_default=False,
        ),
    ]
