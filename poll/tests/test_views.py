from django.test import TestCase
from django.contrib.sessions.models import Session

from poll.models import Country
from poll.views import  get_four_random_countries,\
                        RESULT_WARNING_MESSAGE_NO_SCORE,\
                        RESULT_WARNING_MESSAGE_BAD_EMAIL,\
                        RESULT_SUCCESS_MESSAGE_EMAIL_SENT,\
                        RESULT_MESSAGE_SCORE
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

# POST
    def test_right_answer_saves_score(self):
        response = self.client.get('/poll/')
        session = Session.objects.first().get_decoded()

        self.assertEqual(Session.objects.count(), 1)
        self.assertEqual(session['score'], 0)

        country = Country.objects.get(id = session['answer_id'])
        self.client.post('/poll/', data = {'answer' : country.name})
        session = Session.objects.first().get_decoded()

        self.assertEqual(session['score'], 1)

    def test_wrong_answer_redirects(self):
        response = self.client.get('/poll/')
        response = self.client.post('/poll/', data = {'answer' : 'wrong answer'})
        self.assertRedirects(response, '/poll/result/')

    def test_wrong_answer_not_increase_score(self):
        response = self.client.get('/poll/')
        response = self.client.post('/poll/', data = {'answer' : 'wrong answer'})
        session = Session.objects.first().get_decoded()

        self.assertEqual(session['score'], 0)


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

class TestCountriesByRegionsView(TestCase):
    def setUp(self):
        create_some_countries()

    def test_template_used(self):
        response = self.client.get('/poll/list/')
        self.assertTemplateUsed(response, 'poll/country_by_region.html')


class TestResultView(TestCase):
    def set_session_score(self, score):
        session = self.client.session
        session['score'] = score
        session.save()

    def assert_score_equal(self, response, score):
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), RESULT_MESSAGE_SCORE+str(score))

    def test_uses_right_template(self):
        response = self.client.get('/poll/result/')
        self.assertTemplateUsed(response, 'poll/result.html')

    def test_shows_correct_score(self):
        correct_score = 5
        self.set_session_score(correct_score)
        response = self.client.get('/poll/result/')
        self.assert_score_equal(response, correct_score)

    # def test_shows_default_score(self):
    #     response = self.client.get('/poll/result/')
    #     self.assertEqual(response.context.get('score'), 'nothing')

    def test_post_gets_warning_message_when_no_score(self):
        response = self.client.post('/poll/result/', data = {'email':'a@gmail.com'})
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), RESULT_WARNING_MESSAGE_NO_SCORE)

    def test_post_gets_warning_when_bad_email(self):
        self.set_session_score(1)
        response = self.client.post('/poll/result/')
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), RESULT_WARNING_MESSAGE_BAD_EMAIL)

    def test_post_gets_success_message(self):
        self.set_session_score(1)
        response = self.client.post('/poll/result/', data = {'email':'a@gmail.com'})
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), RESULT_SUCCESS_MESSAGE_EMAIL_SENT)
