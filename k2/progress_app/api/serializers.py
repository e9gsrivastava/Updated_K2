"""
serializers.py
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from progress_app.models import ProgressReport


class USerSerializer(serializers.ModelSerializer):
    """
    serializing data for User model
    """

    class Meta:
        model = User
        fields = ["id", "username", "email", "date_joined"]


class ProgressReportSerializer(serializers.ModelSerializer):
    """
    serializing data for ProgressReport model
    """

    class Meta:
        model = ProgressReport
        fields = "__all__"
