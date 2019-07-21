from django.test import TestCase

from poll.models import Country
from poll.views import get_four_random_countries
from poll.tests.test_base import create_some_countries


class TestIndexView(TestCase):
    def test_view_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'poll/index.html')


class TestPollView(TestCase):
    def setUp(self):
        create_some_countries()

    def test_view_returns_correct_html(self):
        response = self.client.get('/poll/')
        self.assertTemplateUsed(response, 'poll/poll.html')

    def test_returns_countries(self):
        response = self.client.get('/poll/')
        list = response.context['items']
        self.assertEqual(len(list), 4)
        for i in list:
            self.assertIsInstance(i, Country)

    def test_image_loaded(self):
        response = self.client.get('/poll/')
        self.assertContains(response, response.context['img'])


class TestFourRandomContries(TestCase):
    def setUp(self):
        create_some_countries()

    def test_returns_four(self):
        self.assertEqual(len(get_four_random_countries()), 4)

    # def test_items_are_random(self):
    #     print('\n\n\n//////\n\n\n')
    #     print(get_four_random_countries())
    #     self.assertNotEqual(get_four_random_countries(), get_four_random_countries())

    def test_items_are_unique(self):
        for _ in range(10):
            items = get_four_random_countries()
            for i in range(4):
                for j in range(i+1,4):
                    self.assertNotEqual(items[i], items[j])
