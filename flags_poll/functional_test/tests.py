from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time

from poll.models import Country
from poll.tests.test_base import create_some_countries

class NewVisitor(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome('C:\\webdrivers\\chromedriver.exe')
        create_some_countries()

    def test(self):
        self.browser.get(self.live_server_url)
        self.assertEqual(self.live_server_url+'/', self.browser.current_url)
        self.assertIn('Countries Poll', self.browser.title)

        start_poll = self.browser.find_element_by_id('start_poll')
        self.assertEqual(start_poll.get_attribute('type'), 'submit')

        start_poll.click()

        # Answers right four times
        num_right_answers = 4
        for i in range(num_right_answers):
            answers = self.browser.find_elements_by_name('answer')
            self.assertEquals(len(answers), 4)

            flag = self.browser.find_element_by_id('flag_image')
            flag_src = flag.get_attribute('src').split('/')[-1]
            country = Country.objects.get(flag_128 = flag_src)
            self.browser.find_element_by_css_selector(f'input[value="{country.name}"]').click()

        # answers wrong
        answers = self.browser.find_elements_by_name('answer')
        self.assertEquals(len(answers), 4)

        flag = self.browser.find_element_by_id('flag_image')
        flag_src = flag.get_attribute('src').split('/')[-1]
        country = Country.objects.get(flag_128 = flag_src)

        # clicks wrong answer
        if answers[0].get_attribute('value') == country.name:
            answers[1].click()
        else:
            answers[0].click()
        time.sleep(10)
        self.assertIn('Your score: 4', self.browser.find_element_by_id('result').text)
        email_input = self.browser.find_element_by_id("email_input_id")
        email = 'a@gmail.com'
        email_input.send_keys(email).send_keys(keys.ENTER)
        mail = mail.outbox[0]
        self.assertEqual(email, mail.to)


    def tearDown(self):
        self.browser.quit()
