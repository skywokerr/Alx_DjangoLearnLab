from django.test import TestCase
from rest_framework.test import APIClient,APITestCase
# Create your tests here.

class TestView(APITestCase):
    def setUp(self):
        client = APIClient()
        
    def test_user_existing_notifications(self):
        pass