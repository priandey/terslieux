from django.db import models

from user.models import Volunteer, Moderator


class Status(models.Model):
    activity = models.CharField(max_length=255, null=True)
    open_date = models.DateTimeField(auto_now_add=True)
    close_date = models.DateTimeField()
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE, null=True)

class Location(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)
    volunteers = models.ForeignKey(Volunteer, on_delete=models.CASCADE, null=True)
    moderator = models.ForeignKey(Moderator, on_delete=models.CASCADE)