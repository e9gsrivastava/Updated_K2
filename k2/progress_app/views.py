from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DetailView, TemplateView
from django.http import Http404
from django.contrib.auth.models import User
from .models import ProgressReport
from .forms import ProgressReportForm
from django.db.models import Avg


class LoginView(LoginView):
    template_name = "progress_app/login.html"

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return redirect(reverse_lazy("progress_app:overall_progress"))

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("progress_app:login")

class StudentListView(LoginRequiredMixin, ListView):
    model = ProgressReport
    template_name = "progress_app/student_list.html"
    context_object_name = "progress_reports"
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("user")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = User.objects.all()
        return context

class UpdateProgressReportView(UpdateView):
    model = ProgressReport
    form_class = ProgressReportForm
    template_name = "progress_app/update_progress_report.html"
    success_url = reverse_lazy("progress_app:student_list")

class StudentDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "progress_app/student_detail.html"
    context_object_name = "user"

    def get_object(self, queryset=None):
        username = self.kwargs.get("username", None)
        users = User.objects.filter(username=username)

        if not users.exists():
            raise Http404("User not found")

        return users.first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["progress_reports"] = ProgressReport.objects.filter(user=self.object)
        return context

class ProgressGraphView(LoginRequiredMixin, TemplateView):
    template_name = "progress_app/progress_graph.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_users = User.objects.filter(is_superuser=False)

        attendance_data = {}
        for user in all_users:
            progress_reports = ProgressReport.objects.filter(user=user)
            percentages = [report.attendance / 100.0 for report in progress_reports]
            attendance_data[user.username] = percentages

        context["attendance_data"] = attendance_data
        return context

class MarksheetView(LoginRequiredMixin, TemplateView):
    template_name = "progress_app/marksheet.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_users = User.objects.filter(is_superuser=False)

        mark_data = {}
        for user in all_users:
            progress_reports = ProgressReport.objects.filter(user=user)
            marks = [report.marks / 100.0 for report in progress_reports]
            mark_data[user.username] = marks

        context["mark_data"] = mark_data
        return context

class AssignmentReportView(LoginRequiredMixin, TemplateView):
    template_name = "progress_app/assignment_report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_users = User.objects.filter(is_superuser=False)

        assignment_data = {}
        for user in all_users:
            progress_reports = ProgressReport.objects.filter(user=user)
            assignments = [report.assignment / 100.0 for report in progress_reports]
            assignment_data[user.username] = assignments

        context["assignment_data"] = assignment_data
        return context

class OverallProgressView(LoginRequiredMixin, TemplateView):
    template_name = "progress_app/overall_progress.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        

        all_users = User.objects.filter(is_superuser=False)

        overall_data = {}
        for user in all_users:
            progress_reports = ProgressReport.objects.filter(user=user)

            if progress_reports:
                attendance_aggregate = progress_reports.aggregate(average=Avg("attendance"))
                average_attendance = attendance_aggregate["average"]
                attendance_percentage = average_attendance / 100.0
            else:
                attendance_percentage = 0

            if progress_reports:
                marks_aggregate = progress_reports.aggregate(average=Avg("marks"))
                average_marks = marks_aggregate["average"]
                marks_percentage = average_marks / 100.0
            else:
                marks_percentage = 0

            if progress_reports:
                assignment_aggregate = progress_reports.aggregate(average=Avg("assignment"))
                average_assignment = assignment_aggregate["average"]
                assignment_percentage = average_assignment / 100.0
            else:
                assignment_percentage = 0

            overall_data[user.username] = (attendance_percentage + marks_percentage + assignment_percentage) / 3

        context["overall_data"] = overall_data
        return context
