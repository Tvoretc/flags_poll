from selenium import webdriver
from django.test import LiveServerTestCase
import time

class NewVisitor(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome('C:\\webdrivers\\chromedriver.exe')

    def test(self):
        self.browser.get(self.live_server_url)
        # self.assertEqual('http://localhost:8000/', self.browser.current_url)
        self.assertIn('Flags Poll', self.browser.title)

    def tearDown(self):
        self.browser.quit()
