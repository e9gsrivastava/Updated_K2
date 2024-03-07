"""this is Django ORM model"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg


class ProgressReport(models.Model):
    """this is model for Progress report of User"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    week_number = models.PositiveIntegerField()
    attendance = models.PositiveIntegerField()
    assignment = models.PositiveIntegerField()
    marks = models.PositiveIntegerField()
    comments = models.TextField()

    # def get_trainee_attendance(self):
    #     """to get the trainee's attendance data"""
    #     all_users = User.objects.filter(is_superuser=False)

    #     attendance_data = {}
    #     for user in all_users:
    #         progress_reports = ProgressReport.objects.filter(user=user)
    #         percentages = [report.attendance / 100.0 for report in progress_reports]
    #         attendance_data[user.username] = percentages

    #     return attendance_data
    



    
    def get_trainee_attendance(self, progress_reports):
        """To get the trainee's assignment data"""
        all_users = [report.user for report in progress_reports if not report.user.is_superuser]

        attendance_data = {}
        for user in all_users:
            progress_reports     = ProgressReport.objects.filter(user=user)
            percentages = [report.attendance / 100.0 for report in progress_reports]
            attendance_data[user.username] = percentages

        return attendance_data



    # def get_trainee_marks(self):
    #     """to get the trainee's marks data"""
    #     all_users = User.objects.filter(is_superuser=False)

    #     mark_data = {}
    #     for user in all_users:
    #         progress_reports = ProgressReport.objects.filter(user=user)
    #         marks = [report.marks / 100.0 for report in progress_reports]
    #         mark_data[user.username] = marks

    #     return mark_data
    



    def get_trainee_marks(self, progress_reports):
        """To get the trainee's assignment data"""
        all_users = [report.user for report in progress_reports if not report.user.is_superuser]

        mark_data = {}
        for user in all_users:
            user_reports = ProgressReport.objects.filter(user=user)
            marks = [report.marks / 100.0 for report in user_reports]
            mark_data[user.username] = marks

        return mark_data

    # def get_trainee_assignment(self,progress_reports):
    #     """to get the trainee's assignment data"""
    #     # all_users = User.objects.filter(is_superuser=False)
    #     all_users = [report.user for report in progress_reports if not report.user.is_superuser]

    #     assignment_data = {}
    #     for user in all_users:
    #         # progress_reports = ProgressReport.objects.filter(user=user)
    #         assignments = [report.assignment / 100.0 for report in progress_reports]
    #         assignment_data[user.username] = assignments

    #     return assignment_data



    def get_trainee_assignment(self, progress_reports):
        """To get the trainee's assignment data"""
        all_users = [report.user for report in progress_reports if not report.user.is_superuser]

        assignment_data = {}
        for user in all_users:
            user_reports = ProgressReport.objects.filter(user=user)
            assignments = [report.assignment / 100.0 for report in user_reports]
            assignment_data[user.username] = assignments

        return assignment_data


    @classmethod
    def get_trainee_overall_score(cls, progress_reports):
        """to get the trainee's overall data"""
        # all_users = User.objects.filter(is_superuser=False)
        all_users = [report.user for report in progress_reports if not report.user.is_superuser]
        overall_data = {}
        for user in all_users:
            progress_reports = ProgressReport.objects.filter(user=user)

            if progress_reports:
                attendance_aggregate = progress_reports.aggregate(
                    average=Avg("attendance")
                )
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
                assignment_aggregate = progress_reports.aggregate(
                    average=Avg("assignment")
                )
                average_assignment = assignment_aggregate["average"]
                assignment_percentage = average_assignment / 100.0
            else:
                assignment_percentage = 0

            overall_data[user.username] = (
                attendance_percentage + marks_percentage + assignment_percentage
            ) / 3

        return overall_data
