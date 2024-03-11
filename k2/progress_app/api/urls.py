"""
urls.py
"""
from django.urls import path, include
from progress_app.api import views

urlpatterns = [
    path("user/", views.UserList.as_view()),
    path("user/<int:pk>/", views.UserDetail.as_view()),
    path("pr/", views.ProgressReportListCreateAPIView.as_view()),
    path("pr/<int:pk>/", views.ProgressReportDetailCreateAPIView.as_view()),
    path("api-auth/", include("rest_framework.urls")),
]
