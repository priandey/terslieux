from django.db import models

from django.contrib.auth.models import User
from location.models import Location


class UserFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorite")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="favorited")
