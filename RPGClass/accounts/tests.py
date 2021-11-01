from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Create your tests here.
#
def test_login(self):
    with self.browser("index") as page:
        elem = page.find_element_by_id('username')
        elem.send_keys('testuser' + Keys.RETURN)
        elem = page.find_element_by_id('session_name')
        self.assertIsNotNone(elem)