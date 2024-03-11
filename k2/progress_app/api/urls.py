"""
urls.py
"""
from django.urls import path, include
from progress_app.api import views

urlpatterns = [
    path("progress_app/user/", views.UserList.as_view()),
    path("progress_app/user/<int:pk>/", views.UserDetail.as_view()),
    path(
        "progress_app/progress-report/", views.ProgressReportListCreateAPIView.as_view()
    ),
    # path("progress_app/progress-report/<int:pk>/", views.ProgressReportDetailCreateAPIView.as_view()),
    path(
        "progress_app/progress-report/<slug:slug>/",
        views.ProgressReportDetailCreateAPIView.as_view(),
    ),
    path(
        "progress_app/overall-progress/",
        views.OverallProgressAPIView.as_view(),
        name="overall_progress_api",
    ),
    path(
        "progress_app/overall-progress/<slug:slug>/",
        views.OverallProgressDetailAPIView.as_view(),
    ),
    path("api-auth/", include("rest_framework.urls")),
]
