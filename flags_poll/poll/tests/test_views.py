from django.test import TestCase

class indexViewTest(TestCase):
    def test_view_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'poll/index.html')

class pollViewTest(TestCase):
    def test_view_returns_correct_html(self):
        response = self.client.get('/poll/')
        self.assertTemplateUsed(response, 'poll/poll.html')
