from django.test import TestCase

from location.forms import LocationForm


class TestLocationForm(TestCase):
    def test_location_creation_form(self):
        form_data = {
            'name'       : 'NewLoc',
            'description': 'A New location'
        }
        form = LocationForm(data=form_data)
        self.assertTrue(form.is_valid())
