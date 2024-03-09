import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from progress_app.models import ProgressReport
from django.db import IntegrityError

class Command(BaseCommand):
    help = "generate random data for progress reports"

    def handle(self, *args, **options):
        self.generate_random_data()

    def generate_random_data(self):
        trainee_names = ["Akbar", "Shivansh", "Kunal", "Akash", "Gaurav"]
        total_trainees = 10000

        progress_reports = []

        for i in range(total_trainees):
            name = random.choice(trainee_names)
            first_name = f"name{i}"
            base_username = f"e9{name.lower()}"
            username = base_username + str(i)

            while User.objects.filter(username=username).exists():
                i += 1
                username = base_username + str(i)

            try:
                trainee_user, _ = User.objects.get_or_create(
                    username=username,
                    password=f"{name.lower()}_password",
                    first_name=first_name,
                )

                for week_number in range(1, 11):
                    attendance = random.randint(80, 100)
                    assignment = random.randint(60, 100)
                    marks = random.randint(50, 100)
                    comments = f"Week {week_number} good."

                    progress_report = ProgressReport(
                        user=trainee_user,
                        week_number=week_number,
                        attendance=attendance,
                        assignment=assignment,
                        marks=marks,
                        comments=comments,
                    )

                    progress_reports.append(progress_report)

            except IntegrityError as e:
                self.stdout.write(self.style.ERROR(f"IntegrityError: {e}"))

        ProgressReport.objects.bulk_create(progress_reports)

        self.stdout.write(self.style.SUCCESS("Successful."))
