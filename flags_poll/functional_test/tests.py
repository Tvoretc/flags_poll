from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
import time

class NewVisitor(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome('C:\\webdrivers\\chromedriver.exe')

    def test(self):
        self.browser.get(self.live_server_url)
        self.assertEqual(self.live_server_url+'/', self.browser.current_url)
        self.assertIn('Flags Poll', self.browser.title)

        start_poll = self.browser.find_element_by_id('start_poll')
        self.assertEqual(start_poll.get_attribute('type'), 'submit')

        start_poll.click()

        answers = self.browser.find_elements_by_id('answer')
        self.assertEquals(len(answers), 4)

        flag = self.browser.find_element_by_id('flag_image')
        # test image loaded, how?
        # self.assertIn('Flag not found', flag.get_attribute('textContent'))


    def tearDown(self):
        self.browser.quit()
