"""
forms.py
"""

from django import forms
from .models import ProgressReport


class ProgressReportForm(forms.ModelForm):
    """
    form to add marks and comments
    """
    class Meta:
        model = ProgressReport
        fields = ["marks", "comments"]

        widgets = {
            "marks": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
            "comments": forms.Textarea(
                attrs={"class": "form-control"}
            )
        }
