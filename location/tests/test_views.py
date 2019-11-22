from django.test import TestCase

from user.models import CustomUser
from location.models import Location, Status, VolunteerBase, VolunteeringRequest

class TestLocationView(TestCase):
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
        """ If user is volunteer on location, context shoud contain disclaimer """

        self.client.login(email="vol@vol.vol", password="password")
        response = self.client.get("/l/baleine/")
        self.assertTrue(response.context['disclaimer'])

    def test_location_detail_mod_logged(self):
        """ Same as above, but context should contain location_mod """

        self.client.login(email="mod@mod.mod", password="password")
        response = self.client.get("/l/baleine/")
        self.assertTrue(response.context['location_mod'])

    def test_location_creation_get(self):
        """ Get request to location creation view should return a template with a form """

        self.client.login(email="basic@basic.basic", password="password")
        response = self.client.get("/l/create/")
        self.assertTemplateUsed(response, "location/location_creation.html")
        self.assertTrue(response.context['form'])

    def test_location_creation_post_invalid(self):
        self.client.login(email="basic@basic.basic", password="password")
        form_data = {'name': 'NewLoc',
                     'description': 'A New location',
                     'slug': 'new loc wrong url'}
        response = self.client.post('/l/create', data=form_data)
        self.assertEqual(response.url, '/l/create/')

    def test_location_creation_post_valid(self):
        self.client.login(email="basic@basic.basic", password="password")
        form_data = {'name': 'Fibloc',
                     'description': 'A New location'}
        response = self.client.post('/l/create/', data=form_data)
        self.assertRedirects(response, '/l/fibloc/')

    def test_require_volunteering(self):
        self.client.login(email="basic@basic.basic", password="password")
        response = self.client.get('/l/require/baleine')
        self.assertRedirects(response, '/l/baleine/')

    def test_add_status_whithout_permission(self):
        self.client.login(email='basic@basic.basic', password='password')
        response = self.client.get('/l/baleine/status')
        self.assertEqual(response.status_code, 403)

    def test_add_status_with_permission(self):
        self.client.login(email='vol@vol.vol', password='password')
        response = self.client.get('/l/baleine/status')
        self.assertTemplateUsed(response, 'location/status_declaration.html')
        self.assertTrue(response.context['form'])

    def test_add_status_legal_post(self):
        self.client.login(email='vol@vol.vol', password='password')
        form_data = {
            'activity': 'Doing something great',
            'description': 'It will be great, be sure !'
        }
        response = self.client.post('/l/baleine/status', data=form_data)
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.url, "/l/baleine/")

    def test_add_status_illegal_post(self):
        self.client.login(email='basic@basic.basic', password='password')
        form_data = {
            'activity'   : 'Doing something great',
            'description': 'It will be great, be sure !'
        }
        response = self.client.post('/l/baleine/status', data=form_data)
        self.assertEqual(response.status_code, 403)

    def test_close_status_legal(self):
        self.client.login(email='vol@vol.vol', password='password')
        Status.objects.create(location=self.location, activity='Doing things')
        response = self.client.get('/l/baleine/close')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/l/baleine/')

    def test_close_status_illegal(self):
        self.client.login(email='basic@basic.basic', password='password')
        Status.objects.create(location=self.location, activity='Doing stuff')
        response = self.client.get('/l/baleine/close')
        self.assertEqual(response.status_code, 403)

    def test_search_location(self):
        post_data = {
            'research': 'La baleine verte'
        }
        response = self.client.post('/l/search', data=post_data)
        self.assertEqual(response.status_code, 301)

    def test_edit_location_legal_get(self):
        self.client.login(email='mod@mod.mod', password='password')
        response = self.client.get('/l/edit/baleine')
        self.assertTrue(response.context['form'])
        self.assertTrue(response.context['location'] == self.location)

    def test_edit_location_illegal_get(self):
        self.client.login(email='basic@basic.basic', password='password')
        response = self.client.get('/l/edit/baleine')
        self.assertEqual(response.status_code, 403)

    def test_edit_location_legal_post(self):
        self.client.login(email='mod@mod.mod', password='password')
        form_data = {
            'name': 'La baleine bleue',
            'description': 'Une baleine toute bleue'
        }
        response = self.client.post('/l/edit/baleine', data=form_data)
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.url, '/l/baleine/')

    def test_edit_location_illegal_post(self):
        self.client.login(email='basic@basic.basic', password='password')
        form_data = {
            'name'       : 'La baleine bleue',
            'description': 'Une baleine toute bleue'
        }
        response = self.client.post('/l/edit/baleine', data=form_data)
        self.assertEqual(response.status_code, 403)

    def test_delete_location_get(self):
        self.client.login(email="basic@basic.basic", password="password")
        response = self.client.get('/l/delete/baleine')
        self.assertTrue(response.status_code, 403)

    def test_delete_location_legal(self):
        self.client.login(email='mod@mod.mod', password='password')
        response = self.client.post('/l/delete/baleine')
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.url, '/private/')
