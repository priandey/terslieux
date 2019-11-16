from django.test import TestCase
from django.utils import timezone

from user.models import CustomUser
from location.models import Location, Status, VolunteerBase, VolunteeringRequest

class TestStatisticViews(TestCase):
    def setUp(self):
        self.moderator = CustomUser.objects.create_user(email="mod@mod.mod", password="password")
        self.basic_user = CustomUser.objects.create_user(email="basic@basic.basic", password="password")
        self.volunteer = CustomUser.objects.create_user(email="vol@vol.vol", password="password")
        self.volunteering_request = VolunteeringRequest.objects.create(
                sender=self.moderator,
                receiver=self.volunteer,
                validated=True
        )

        self.location = Location.objects.create(
                name="La baleine verte",
                description="Une baleine ni bleue, ni rouge",
                moderator=self.moderator,
                slug="baleine")

        close_date = timezone.now().replace(hour=timezone.now().hour + 1)  # Putting a close date an hour later

        self.status = Status.objects.create(
                activity="Salsa Dancing",
                description="Dancing Salsa !",
                close_date=close_date,
                volunteer=self.volunteer,
                location=self.location
        )

        self.volunteerBase = VolunteerBase.objects.create(
                volunteer=self.volunteer,
                location=self.location,
                is_active=True,
                volunteering_request=self.volunteering_request
        )

    def test_generate_pdf_legal(self):
        self.client.login(email="mod@mod.mod", password="password")
        response = self.client.get('/statistic/baleine')
        self.assertEqual(response.status_code, 200)

    def test_generate_pdf_illegal(self):
        self.client.login(email='basic@basic.basic', password='password')
        response = self.client.get('/statistic/baleine')
        self.assertEqual(response.status_code, 403)
