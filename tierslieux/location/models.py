from django.db import models
from django.utils import timezone
from user.models import CustomUser


class Location(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    volunteers = models.ManyToManyField(CustomUser, through='VolunteerBase', related_name="volunteers")
    moderator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="location")
    slug = models.SlugField(unique=True)

class Status(models.Model):
    activity = models.CharField(max_length=255, default="Ouvert")
    open_date = models.DateTimeField(auto_now_add=True)
    close_date = models.DateTimeField(null=True)
    volunteer = models.ForeignKey(CustomUser, related_name='opened', on_delete=models.SET_NULL, null=True) #TODO : Edit this to point to VolunteerBase
    location = models.ForeignKey(Location, related_name='status', on_delete=models.CASCADE)

    def __repr__(self):
        return f'{self.activity} at {self.open_date}'

    def close(self):
        self.close_date = timezone.now()
        self.save()

    @property
    def is_opened(self):
        if not self.close_date:
            return True
        else:
            return False

    @property
    def open_time(self): #TODO : Return time in day/hours/minutes
        if self.close_date:
            opened_time = self.close_date - self.open_date
            return opened_time.total_seconds()


class VolunteeringRequest(models.Model): #TODO : Volunteer can volunteer twice in a location
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="request_sent")
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="request_received")
    comment = models.CharField(max_length=255, null=True, default="Je souhaiterais être bénévole pour votre association")
    validated = models.BooleanField(null=True)
    date = models.DateTimeField(auto_now_add=True)

    @property
    def sender_is_mod(self):
        if self.volunteer_base.get().location.moderator == self.sender:
            return True
        else:
            return False
class VolunteerBase(models.Model): #TODO : Change VolunteerBase into Volunteer and field volunteer to user
    volunteer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    volunteering_request = models.ForeignKey(VolunteeringRequest, on_delete=models.CASCADE, related_name="volunteer_base")
