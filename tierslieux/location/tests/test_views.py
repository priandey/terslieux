from django.test import TestCase

from user.models import CustomUser
from location.models import Location, Status, VolunteerBase, VolunteeringRequest
from location.forms import LocationForm

class TestLocation(TestCase):
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

        self.volunteerBase = VolunteerBase.objects.create(
                volunteer=self.volunteer,
                location=self.location,
                is_active=True,
                volunteering_request=self.volunteering_request
        )

    def test_location_detail_anonymous(self):
        """ Not logged user should access a specific template """
        Status.objects.create(
                volunteer=self.volunteer,
                location=self.location
        )
        response = self.client.get('/l/baleine/')
        self.assertTemplateNotUsed(response, 'location/location_detail_logged.html')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['opened'])

    def test_location_detail_logged(self):
        """ Logged user should access a specific template """
        self.client.login(email="basic@basic.basic", password="password")
        response = self.client.get('/l/baleine/')
        self.assertTemplateUsed(response, 'location/location_detail_logged.html')

    def test_location_detail_vol_logged(self):
        """ """
        self.client.login(email="vol@vol.vol", password="password")
        response = self.client.get("/l/baleine/")
        self.assertTrue(response.context['disclaimer'])

    def test_location_detail_mod_logged(self):
        """ """
        self.client.login(email="mod@mod.mod", password="password")
        response = self.client.get("/l/baleine/")
        self.assertTrue(response.context['location_mod'])

    def test_location_creation_get(self):
        self.client.login(email="basic@basic.basic", password="password")
        response = self.client.get("/l/create/")
        self.assertTemplateUsed(response, "location/location_creation.html")
        self.assertTrue(response.context['form'])

    def test_location_creation_form(self):
        form_data = {
            'name'       : 'NewLoc',
            'description': 'A New location',
            'slug'       : 'newloc'
        }
        form = LocationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_location_creation_form_invalid(self):
        form_data = {
            'name'       : 'NewLoc',
            'description': 'A New location',
            'slug'       : 'new loc wrong slug'
        }
        form = LocationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_location_creation_post_invalid(self):
        self.client.login(email="basic@basic.basic", password="password")
        form_post = {'name': 'NewLoc',
                     'description': 'A New location',
                     'slug': 'new loc wrong url'}
        response = self.client.post('/l/create', data=form_post)
        self.assertEqual(response.url, '/l/create/')

    def test_location_creation_post_valid(self):
        self.client.login(email="basic@basic.basic", password="password")
        form_post = {'name': 'NewLoc',
                     'description': 'A New location',
                     'slug': 'testloc'}
        response = self.client.post('/l/create', data=form_post)
        self.assertEqual(response.url, '/private/')

    def test_require_volunteering(self):
        self.client.login(email="basic@basic.basic", password="password")
        self.client.get('/require/baleine')