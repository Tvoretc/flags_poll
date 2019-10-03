from django.test import TestCase

# import unittest

from poll.forms import ScoreRecordForm


class ScoreRecordFormTest(TestCase):

    def test_form_invalid_for_bad_email(self):
        form = ScoreRecordForm(data={'email':'123'})
        self.assertFalse(form.is_valid())

    def test_form_valid_when_email_given(self):
        form = ScoreRecordForm(data={'email':'a@gmail.com'})
        self.assertTrue(form.is_valid())
