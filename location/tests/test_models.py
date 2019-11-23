from django.test import TestCase

from location.models import Status, Location, VolunteeringRequest, VolunteerBase
from user.models import CustomUser

class TestStatus(TestCase):
    """ Test core methods of Status model """

    def setUp(self):
        self.moderator = CustomUser.objects.create_user(email="mod@mod.mod", password="password")
        self.volunteer = CustomUser.objects.create_user(email="vol@vol.vol", password="password")

        self.location = Location.objects.create(
                name="La baleine verte",
                description="Une baleine ni bleue, ni rouge",
                moderator=self.moderator,
                slug="baleine")

        self.status = Status.objects.create(
                activity = 'Danses de la joie',
                description = "Une danse permettant d'exprimer son bonheur",
                volunteer = self.volunteer,
                location = self.location
        )

    def test_status_is_opened_true(self):
        self.assertTrue(self.status.is_opened)

    def test_status_is_opened_false(self):
        self.status.close()
        self.assertFalse(self.status.is_opened)

    def test_close(self):
        self.status.close()
        self.assertTrue(self.status.close_date)

    def test_open_time_legal(self):
        self.status.close()
        self.assertTrue(self.status.open_time)


class TestVolunteeringRequest(TestCase):
    """ Test core method of VolunteeringRequest model """

    def setUp(self):
        self.moderator = CustomUser.objects.create_user(email="mod@mod.mod", password="password")
        self.basic_user = CustomUser.objects.create_user(email="basic@basic.basic", password="password")

        self.location = Location.objects.create(
                name="La baleine verte",
                description="Une baleine ni bleue, ni rouge",
                moderator=self.moderator,
                slug="baleine")

    def test_sender_is_mod_true(self):
        self.volunteering_request = VolunteeringRequest.objects.create(
                sender=self.moderator,
                receiver=self.basic_user
        )

        self.base = VolunteerBase.objects.create(
                volunteer=self.basic_user,
                location=self.location,
                volunteering_request=self.volunteering_request
        )
        self.assertTrue(self.volunteering_request.sender_is_mod)

    def test_sender_is_mod_false(self):
        self.volunteering_request = VolunteeringRequest.objects.create(
                sender= self.basic_user,
                receiver=self.moderator
        )

        self.base = VolunteerBase.objects.create(
                volunteer=self.basic_user,
                location=self.location,
                volunteering_request=self.volunteering_request
        )
        self.assertFalse(self.volunteering_request.sender_is_mod)
