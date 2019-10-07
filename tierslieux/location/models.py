from django.db import models

from user.models import Volunteer, Moderator, CustomUser


class Location(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    volunteers = models.ManyToManyField(Volunteer, through='VolunteerBase', related_name="volunteers")
    moderator = models.ForeignKey(Moderator, on_delete=models.CASCADE, related_name="location")
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

class VolunteeringRequest(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="request_sent")
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="request_received")
    comment = models.CharField(max_length=255, null=True, default="Je souhaiterais être bénévole pour votre association")
    validated = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

class VolunteerBase(models.Model):
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    volunteering_request = models.ForeignKey(VolunteeringRequest, on_delete=models.CASCADE, related_name="volunteer_base")
