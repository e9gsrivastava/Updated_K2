"""this is view for progress_app"""

from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DetailView, TemplateView
from django.http import Http404
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from progress_app.models import ProgressReport
from .forms import ProgressReportForm


class CustomLoginView(LoginView):
    "This class is used for login"
    template_name = "progress_app/login.html"

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return redirect(reverse_lazy("progress_app:overall_progress"))


class CustomLogoutView(LogoutView):
    """this is to logout"""

    next_page = reverse_lazy("progress_app:login")


class UpdateProgressReportView(UpdateView):
    """this is to update the Students marks and comments"""

    model = ProgressReport
    form_class = ProgressReportForm
    template_name = "progress_app/update_progress_report.html"

    def get_object(self, queryset=None):
        progress_report_id = self.kwargs.get("pk", None)
        progress_report = get_object_or_404(ProgressReport, id=progress_report_id)
        return progress_report

    def get_success_url(self):
        return reverse_lazy(
            "progress_app:student_detail",
            kwargs={"username": self.object.user.username},
        )


class StudentDetailView(LoginRequiredMixin, DetailView):
    """this shows the detiled view of a single students progress
    which includes attendance, marksgiven by metor, assignment and comments given by mentor
    """

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


class AttendanceReportView(LoginRequiredMixin, TemplateView):
    """this shows the attendance submission in percentage weekwise"""

    template_name = "progress_app/progress_graph.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["attendance_data"] = ProgressReport().get_trainee_attendance()
        return context


class MarksheetView(LoginRequiredMixin, TemplateView):
    """this shows the marks given by mentor"""

    template_name = "progress_app/marksheet.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["mark_data"] = ProgressReport().get_trainee_marks()
        return context


class AssignmentReportView(LoginRequiredMixin, TemplateView):
    """this shows the assigment submission reprt in percentage"""

    template_name = "progress_app/assignment_report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["assignment_data"] = ProgressReport().get_trainee_assignment()
        return context


class OverallProgressView(LoginRequiredMixin, TemplateView):
    """this shows the overall progress of the student"""

    template_name = "progress_app/overall_progress.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["overall_data"] = ProgressReport().get_trainee_overall_score()
        return context
