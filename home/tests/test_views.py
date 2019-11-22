from django.test import TestCase

from location.models import Location, Status
from user.models import CustomUser


class TestHomeViews(TestCase):
    def setUp(self):
        self.moderator = CustomUser.objects.create_user(email="mod@mod.mod", password="password")
        self.volunteer = CustomUser.objects.create_user(email="vol@vol.vol", password="password")

        self.location = Location.objects.create(
                name="La baleine verte",
                description="Une baleine ni bleue, ni rouge",
                moderator=self.moderator,
                slug="baleine")

        self.status = Status.objects.create(
                activity='Danses de la joie',
                description="Une danse permettant d'exprimer son bonheur",
                volunteer=self.volunteer,
                location=self.location
        )

    def test_home_with_open_loc(self):
        """At least one location opened"""
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home/index.html')
        self.assertIn(self.location, response.context['opened_locations'])

    def test_home_no_open_loc(self):
        """ No locations currently opened"""
        self.status.close()
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home/index.html')
        self.assertNotIn(self.location, response.context['opened_locations'])

    def test_autocomplete_with_prop(self):
        """ Testing view with matching input """
        response = self.client.get('/autocomplete/', data={'term': 'verte'})
        self.assertJSONEqual(str(response.content, encoding='utf8'), [self.location.name,])

    def test_autocomplete_without_prop(self):
        """ Testing view without matching input """
        response = self.client.get('/autocomplete/', data={'term': 'gloub'})
        self.assertJSONEqual(str(response.content, encoding='utf8'), [])


