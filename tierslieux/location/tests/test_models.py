from django.test import TestCase

from user.models import CustomUser
from location.models import Location, Status

class TestLocation(TestCase):
    def setUp(self):
        moderator = CustomUser.objects.create(email="toust@toust.touse")
        Location.objects.create(
                name="La baleine verte",
                description="Une baleine ni bleue, ni rouge",
                moderator=moderator,
                slug="baleine"
        )