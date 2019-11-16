from django.test import TestCase

from userlocations.models import UserFavorite
from user.models import CustomUser
from location.models import Location, VolunteeringRequest, VolunteerBase


class TestUserLocationViews(TestCase):
    def setUp(self):
        self.moderator = CustomUser.objects.create_user(email="mod@mod.mod", password="password")
        self.basic_user = CustomUser.objects.create_user(email="basic@basic.basic", password="password")
        self.volunteer = CustomUser.objects.create_user(email="vol@vol.vol", password="password")
        self.volunteering_request = VolunteeringRequest.objects.create(
                sender=self.moderator,
                receiver=self.volunteer,
                validated=False
        )

        self.location = Location.objects.create(
                name="La baleine verte",
                description="Une baleine ni bleue, ni rouge",
                moderator=self.moderator,
                slug="baleine")

        self.volunteerBase = VolunteerBase.objects.create(
                volunteer=self.volunteer,
                location=self.location,
                is_active=True,
                volunteering_request=self.volunteering_request
        )

        self.favorite = UserFavorite.objects.create(
                user=self.moderator,
                location=self.location
        )

    def test_locations_no_vol(self):
        """ Test locations views with user not being volunteer in any  location """
        self.client.login(email="mod@mod.mod", password='password')
        response = self.client.get('/private/')
        self.assertTemplateUsed(response, 'userlocations/locations.html')
        self.assertTrue(response.context['favorites'])
        self.assertTrue(response.context['moderated'], self.location)
        self.assertFalse(response.context['volunteerbase'])

    def test_add_favorite_legal(self):
        """ Location not already in user favorite """
        self.client.login(email="vol@vol.vol", password="password")
        response = self.client.get('/private/new_fav/baleine')
        self.assertRedirects(response, '/l/baleine/')

    def test_add_favorite_illegal(self):
        self.client.login(email="mod@mod.mod", password='password')
        response = self.client.get('/private/new_fav/baleine')
        self.assertEqual(response.status_code, 403)

    def test_accept_volunteering_legal(self):
        self.client.login(email="vol@vol.vol", password="password")
        response = self.client.get('/private/accept/{}'.format(self.volunteering_request.pk))
        self.assertRedirects(response, '/private/')

    def test_accept_volunteering_illegal(self):
        self.client.login(email="basic@basic.basic", password="password")
        response = self.client.get('/private/accept/{}'.format(self.volunteering_request.pk))
        self.assertEqual(response.status_code, 403)
