from django.db import models
from django.contrib.auth.models import User

class ProgressReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    week_number = models.PositiveIntegerField()
    attendance = models.PositiveIntegerField()
    assignment = models.PositiveIntegerField()
    marks = models.PositiveIntegerField()
    comments = models.TextField()
