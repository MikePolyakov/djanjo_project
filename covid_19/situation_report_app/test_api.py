from rest_framework.test import APIClient
from django.test.client import RequestFactory
from django.test import TestCase


class ApiTest(TestCase):
    def setUp(self):
        client = APIClient()
        client.login(username='author', password='user2020')

    def test_new_place(self):
        factory = RequestFactory()
        print('factory new place test')
        request = factory.post('/api/v0/places/', {'place_name': 'The Land of Oz'})
        response = self.client.get('/api/v0/places/')
        self.assertEqual(response.status_code, 200)
