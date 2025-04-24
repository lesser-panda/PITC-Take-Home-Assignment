from django.contrib import admin
from stat_analysis import models as stat_analysis_models


admin.site.register([
    stat_analysis_models.Report,
    stat_analysis_models.JobReportResult,
    stat_analysis_models.OrderReportResult,
])
