from django.db import models

from user.models import Volunteer, Moderator


class Location(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    volunteers = models.ManyToManyField(Volunteer, related_name="volunteers")
    moderator = models.ForeignKey(Moderator, on_delete=models.CASCADE)
    slug = models.SlugField()

#TODO : Association table => is_active / request
#TODO : modèle request (sender/receiver) + date
#TODO : Renseigner sur les token

class Status(models.Model):
    activity = models.CharField(max_length=255, default="Ouvert")
    open_date = models.DateTimeField(auto_now_add=True)
    close_date = models.DateTimeField(null=True) #TODO : Add function to edit this field when closing location
    volunteer = models.ForeignKey(Volunteer, related_name='opened', on_delete=models.SET_NULL, null=True)
    location = models.ForeignKey(Location, related_name='status', on_delete=models.CASCADE)

    def __repr__(self):
        return f'{self.activity} at {self.open_date}'