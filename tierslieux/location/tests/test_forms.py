from django.test import TestCase

from location.forms import LocationForm


class TestLocationForm(TestCase):
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
