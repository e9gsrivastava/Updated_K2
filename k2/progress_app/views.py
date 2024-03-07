"""this is view for progress_app"""

from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DetailView, TemplateView
from django.http import Http404
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from progress_app.models import ProgressReport
from .forms import ProgressReportForm
from django.views.generic import ListView


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
    login_url = reverse_lazy("progress_app:login")

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
    """this shows the detailed view of a single student's progress
    which includes attendance, marksgiven by mentor, assignment and comments given by mentor
    """

    User = get_user_model()
    model = User
    template_name = "progress_app/student_detail.html"
    login_url = reverse_lazy("progress_app:login")
    context_object_name = "user"
    paginate_by = 8

    def get_object(self, queryset=None):
        user_model = get_user_model()
        username = self.kwargs.get("username", None)
        users = user_model.objects.filter(username=username)

        if not users.exists():
            raise Http404("User not found")

        return users.first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        progress_reports = ProgressReport.objects.filter(user=self.object)
        paginator = Paginator(progress_reports, self.paginate_by)
        page = self.request.GET.get("page")
        try:
            progress_reports_page = paginator.page(page)
        except PageNotAnInteger:
            progress_reports_page = paginator.page(1)
        except EmptyPage:
            progress_reports_page = paginator.page(paginator.num_pages)

        context["progress_reports"] = progress_reports_page
        return context



    
class AttendanceReportView(LoginRequiredMixin, ListView):
    """This shows the assignment submission report in percentage"""

    model = ProgressReport
    template_name = "progress_app/common_progress.html"
    login_url = reverse_lazy("progress_app:login")
    paginate_by = 100

    def get_queryset(self):
        all_users = User.objects.filter(is_superuser=False)
        return ProgressReport.objects.filter(user__in=all_users)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["data_type"] = "Attendance"
        temp = ProgressReport().get_trainee_attendance(context["object_list"])
        context["overall_data"] = temp
        return context
    


    
class MarksheetView(LoginRequiredMixin, ListView):
    """This shows the assignment submission report in percentage"""

    model = ProgressReport
    template_name = "progress_app/common_progress.html"
    login_url = reverse_lazy("progress_app:login")
    paginate_by = 100

    def get_queryset(self):
        all_users = User.objects.filter(is_superuser=False)
        return ProgressReport.objects.filter(user__in=all_users)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["data_type"] = "Marks"
        temp = ProgressReport().get_trainee_marks(context["object_list"])
        context["overall_data"] = temp
        return context



class AssignmentReportView(LoginRequiredMixin, ListView):
    """This shows the assignment submission report in percentage"""

    model = ProgressReport
    template_name = "progress_app/common_progress.html"
    login_url = reverse_lazy("progress_app:login")
    paginate_by = 100

    def get_queryset(self):
        all_users = User.objects.filter(is_superuser=False)
        return ProgressReport.objects.filter(user__in=all_users)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["data_type"] = "Assignment"
        temp = ProgressReport().get_trainee_assignment(context["object_list"])
        context["overall_data"] = temp
        return context



class OverallProgressView(LoginRequiredMixin, ListView):
    """This shows the overall progress of the student"""

    template_name = "progress_app/overall_progress.html"
    paginate_by = 100
    login_url = reverse_lazy("progress_app:login")
    model = ProgressReport  

    def get_queryset(self):

        all_users = User.objects.filter(is_superuser=False)
        return ProgressReport.objects.filter(user__in=all_users)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        temp = ProgressReport().get_trainee_overall_score(context["object_list"])
        context["overall_data"] = temp
        return context


