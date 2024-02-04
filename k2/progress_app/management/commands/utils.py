import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from progress_app.models import ProgressReport

class Command(BaseCommand):
    help = 'generate random data for progress reports'

    def handle(self, *args, **options):
        self.generate_random_data()

    def generate_random_data(self):
        trainee_names = ["Akbar", "Shivansh", "Kunal", "Akash", "Gaurav"]

        for name in trainee_names:
            first_name = name
            username = f"e9{name.lower()}"
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

                ProgressReport.objects.create(
                    user=trainee_user,
                    week_number=week_number,
                    attendance=attendance,
                    assignment=assignment,
                    marks=marks,
                    comments=comments,
                )

        self.stdout.write(self.style.SUCCESS("Successful."))
