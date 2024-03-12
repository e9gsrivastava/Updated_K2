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
        fields = [ "username", "email"]


class ProgressReportSerializer(serializers.ModelSerializer):
    """
    serializing data for ProgressReport model
    """

    class Meta:
        model = ProgressReport
        fields = ['user','week_number','attendance','assignment','marks','comments','slug']
        read_only_fields = ["slug"]


class OverallProgressSerializer(serializers.Serializer):

    username = serializers.CharField()
    overall_percentage = serializers.FloatField()

    def get_user(self, obj):
        user = getattr(obj, "user", None)
        return getattr(user, "username", None)
