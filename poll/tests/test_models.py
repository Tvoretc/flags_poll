from django.test import TestCase

from poll.models import Country

class TestCountryModel(TestCase):
    def test_db_id(self):
        self.assertEqual(Country.objects.count(), 0)
        Country.objects.create(name = "Afghanistan", code2l='AF', code3l='AFG')
        self.assertEqual(Country.objects.first().id, 1)
