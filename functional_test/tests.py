import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core import mail

from poll.models import Country
from poll.tests.test_base import create_some_countries

import time

class NewVisitor(StaticLiveServerTestCase):
    def setUp(self):
        if os.name == 'nt':
            self.browser = webdriver.Chrome('C:\\webdrivers\\chromedriver.exe')
        else:
            self.browser = webdriver.Chrome()
        create_some_countries()

    def test_poll(self):
        self.browser.get(self.live_server_url)
        self.assertEqual(f'{self.live_server_url}/', self.browser.current_url)
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
            
            self.browser.find_element_by_css_selector(
                f'input[value="{country.name}"]'
            ).click()

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

        # redirected to success page
        self.assertIn('Your score: 4',
            self.browser.find_element_by_css_selector('.success').text)

        # Enters email
        email_input = self.browser.find_element_by_id("id_email")
        email = 'a@gmail.com'
        email_input.send_keys(email)
        email_input.send_keys(Keys.ENTER)

        # checks mailbox
        self.assertEqual(len(mail.outbox), 1)
        sent_mail = mail.outbox[0]
        self.assertEqual([email], sent_mail.to)


    def test_list(self):
        # Go to generic list page
        self.browser.get(f'{self.live_server_url}/poll/generic/')
        self.assertEqual(
            f'{self.live_server_url}/poll/generic/',
            self.browser.current_url
        )

        # Check list is complete
        countries_link = self.browser.find_elements_by_id('id_country')
        countries_link = [item.text for item in countries_link]
        countries = Country.objects.all()
        self.assertEqual(len(countries), len(countries_link))
        for c_in_base in countries:
            self.assertIn(c_in_base.name, countries_link)

        # Visit country page
        country_link = self.browser.find_element_by_id('id_country')
        country = Country.objects.get(name = country_link.text)
        country_link.click()
        self.assertIn(
            f'/poll/country/{country.code3l}',
            self.browser.current_url
        )

        # Check right info on page
        image = self.browser.find_element_by_tag_name('img')
        image_name = image.get_attribute('src').split('/')[-1]
        self.assertEqual(country.flag_128, image_name)


    def tearDown(self):
        self.browser.quit()
