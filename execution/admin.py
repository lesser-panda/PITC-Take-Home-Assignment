from django.contrib import admin
from execution import models as execution_models


admin.site.register([
    execution_models.Job,
    execution_models.JobState,
])
