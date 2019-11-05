from django.db import models

from user.models import CustomUser
from location.models import Location

class UserFavorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="favorite")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="favorited")
