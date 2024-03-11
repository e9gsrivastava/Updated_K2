"""
admin.py
"""
from django.contrib import admin
from .models import ProgressReport


@admin.register(ProgressReport)
class ProgressReportAdmin(admin.ModelAdmin):
    """
    to register PrgoressReport model in admin page
    """

    list_display = (
        "user",
        "week_number",
        "attendance",
        "assignment",
        "marks",
        "comments",
    )
