from django.urls import path
from .views import (
    CustomLoginView,
    CustomLogoutView,
    UpdateProgressReportView,
    AttendanceReportView,
    MarksheetView,
    AssignmentReportView,
    OverallProgressView,
    StudentDetailView,
)

app_name = "progress_app"

urlpatterns = [
    path("", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path(
        "update_progress_report/<int:pk>/",
        UpdateProgressReportView.as_view(),
        name="update_progress_report",
    ),
    path("progress_graph/", AttendanceReportView.as_view(), name="progress_graph"),
    path("marksheet/", MarksheetView.as_view(), name="marksheet"),
    path(
        "assignment_report/", AssignmentReportView.as_view(), name="assignment_report"
    ),
    path("overall_progress/", OverallProgressView.as_view(), name="overall_progress"),
    path(
        "student_detail/<str:username>/",
        StudentDetailView.as_view(),
        name="student_detail",
    ),
]
