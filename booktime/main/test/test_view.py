from django.test import TestCase

class TestPage(TestCase):
    def test_home_page_works(self):
        response = self.client.get("/") #sends a request to the homepage.
        self.assertEqual(response.status_code, 200) #checks if the page loads successfully.
        self.assertTemplateUsed(response, 'home.html') #ensures the correct template is used
        self.assertContains(response, 'BookTime') #verifies that the page contains the shop's name.