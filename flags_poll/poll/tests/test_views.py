from django.test import TestCase

from poll.models import Country
from poll.views import get_four_random_countries

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
        self.assertEqual(len(get_four_random_countries()), 4)

    def test_items_are_random(self):
        print('\n\n\n//////\n\n\n')
        print(get_four_random_countries())
        self.assertNotEqual(get_four_random_countries(), get_four_random_countries())

    def test_items_are_unique(self):
        for _ in range(10):
            items = get_four_random_countries()
            for i in range(4):
                for j in range(i+1,4):
                    self.assertNotEqual(items[i], items[j])
