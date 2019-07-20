from django.test import TestCase

from poll.models import Country
from poll.views import get_four_random_countries


def create_some_countries():
    Country.objects.create(name = "Afghanistan", code2l='AF', code3l='AFG')
    Country.objects.create(name = "Åland Islands", code2l = 'AX', code3l='ALA')
    Country.objects.create(name = "Albania", code2l = 'AL', code3l='ALB')
    Country.objects.create(name = "Algeria", code2l = 'DZ', code3l='DZA')
    Country.objects.create(name = "American Samoa", code2l = 'AS', code3l='ASM')
    Country.objects.create(name = "Andorra", code2l = 'AD', code3l='AND')
    Country.objects.create(name = "Aruba", code2l = 'AW', code3l='ABW')
    Country.objects.create(name = "Australia", code2l = 'AU', code3l='AUS')

class indexViewTest(TestCase):
    def test_view_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'poll/index.html')


class pollViewTest(TestCase):
    def test_view_returns_correct_html(self):
        response = self.client.get('/poll/')
        self.assertTemplateUsed(response, 'poll/poll.html')


class TestFourRandomContries(TestCase):
    def test_returns_four(self):
        create_some_countries()
        self.assertEqual(len(get_four_random_countries()), 4)

    # def test_items_are_random(self):
    #     print('\n\n\n//////\n\n\n')
    #     print(get_four_random_countries())
    #     self.assertNotEqual(get_four_random_countries(), get_four_random_countries())

    def test_items_are_unique(self):
        create_some_countries()
        for _ in range(10):
            items = get_four_random_countries()
            for i in range(4):
                for j in range(i+1,4):
                    self.assertNotEqual(items[i], items[j])
