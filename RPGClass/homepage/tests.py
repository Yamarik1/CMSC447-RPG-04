from django.test import TestCase
from django.urls import reverse


# Create your tests here.

# Test for the skeleton homepage
class TestClass(TestCase):
    # The url found at homepage/menu.html should exist, and will return 200 code
    def test_url_correctness(self):
        response = self.client.get(reverse('homepage:menu'))
        self.assertEqual(response.status_code, 200)
