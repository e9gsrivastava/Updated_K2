"""
views.py
"""
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from .serializers import USerSerializer, ProgressReportSerializer
from progress_app.models import ProgressReport

class UserList(generics.ListCreateAPIView):
    """
    API view for listing and creating Book objects.
    """

    queryset = User.objects.all()
    serializer_class = USerSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting a Book object.
    """

    queryset = User.objects.all()
    serializer_class = USerSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class ProgressReportListCreateAPIView(generics.ListCreateAPIView):
    """
    API view for listing and creating a ProgressReport object.
    """

    queryset = ProgressReport.objects.all()
    serializer_class = ProgressReportSerializer
    # permission_classes = [permissions.IsAuthenticated]


class ProgressReportDetailCreateAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting a ProgressReport object.
    """

    queryset = User.objects.all()
    serializer_class = USerSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
