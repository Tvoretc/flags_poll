from django.test import TestCase

import os
import json
from random import shuffle
from decimal import Decimal

from poll.models import Country

class TestCountryModel(TestCase):
    def test_migration_loaded_countries(self):
        with open(os.path.join('poll', 'migrations', 'countries.json'), 'r') as file:
            loaded_countries = json.load(file)

        self.assertEqual(Country.objects.count(), len(loaded_countries))
        shuffle(loaded_countries)
        loaded_countries = sorted(loaded_countries[:5], key=lambda x: x['id'])

        random_country_ids = list(country['id'] for country in loaded_countries)
        db_countries = Country.objects.filter(id__in = random_country_ids).order_by('pk')

        for db_c, loaded_c in zip(db_countries, loaded_countries):
            loaded_c['latitude'] = Decimal(loaded_c['latitude'])
            loaded_c['longitude'] = Decimal(loaded_c['longitude'])

            for name, value in loaded_c.items():
                self.assertEqual(getattr(db_c, name), value)

            self.assertEqual(getattr(db_c, 'flag_32'), f'{db_c.code2l}-32.png')
            self.assertEqual(getattr(db_c, 'flag_128'), f'{db_c.code2l}-128.png')
