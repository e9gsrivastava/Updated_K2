"""
views.py
"""
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import USerSerializer, ProgressReportSerializer
from progress_app.models import ProgressReport
from rest_framework.pagination import LimitOffsetPagination
from .serializers import OverallProgressSerializer
from rest_framework.response import Response
from rest_framework import status


class UserList(generics.ListCreateAPIView):
    """
    API view for listing and creating Book objects.
    """

    queryset = User.objects.all()
    serializer_class = USerSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting a Book object.
    """

    queryset = User.objects.all()
    serializer_class = USerSerializer


class ProgressReportListCreateAPIView(generics.ListCreateAPIView):
    """
    API view for listing and creating a ProgressReport object.
    """

    queryset = ProgressReport.objects.all()
    serializer_class = ProgressReportSerializer


class ProgressReportDetailCreateAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting a ProgressReport object.
    """

    queryset = ProgressReport.objects.all()
    serializer_class = ProgressReportSerializer
    lookup_field = "slug"


class MyPagination(LimitOffsetPagination):
    """
    For Pagination
    """

    default_limit = 100
    max_limit = 10


class OverallProgressAPIView(generics.ListCreateAPIView):
    """
    API view for listing and creating a Overall Progress object.
    """

    serializer_class = OverallProgressSerializer
    pagination_class = MyPagination

    def get_queryset(self):
        """
        to write queryset
        """
        return ProgressReport.objects.all()

    def list(self, request, *args, **kwargs):
        """
        to calulate dynamically Overall Progress
        """
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            overall_data = ProgressReport.get_trainee_overall_score(page)
            serialized_data = []

            for username, overall_percentage in overall_data.items():
                serialized_data.append(
                    {
                        "username": username,
                        "overall_percentage": overall_percentage * 100,
                    }
                )

            serializer = self.get_serializer(data=serialized_data, many=True)
            serializer.is_valid()

            return self.get_paginated_response(serializer.data)


class OverallProgressDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve and retrieve Overall Progress object.
    """

    serializer_class = OverallProgressSerializer
    pagination_class = MyPagination
    lookup_field = "slug"

    def get_queryset(self):
        """
        to write queryset
        """
        return ProgressReport.objects.all()

    def retrieve(self, request, *args, **kwargs):
        """
        to retrieve Overall Progress
        """
        instance = self.get_object()
        overall_data = ProgressReport.get_trainee_overall_score([instance])
        username = instance.user.username

        if username in overall_data:
            serialized_data = {
                "username": username,
                "overall_percentage": overall_data[username] * 100,
            }

            serializer = self.get_serializer(data=serialized_data)
            serializer.is_valid()

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "User not found in overall data"})

    def retrieve(self, request, *args, **kwargs):
        """
        to destroy Overall Progress
        """
        instance = self.get_object()
        instance.delete()

        return Response(
            {"detail": "Successfully deleted."}, status=status.HTTP_204_NO_CONTENT
        )
