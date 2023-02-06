from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.test import APIClient, APITestCase
from robots.models import Robot


class TestAPIPost(APITestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser('admin', 'admin@testadmin.com', 'testcase')

    def setUp(self):
        self. user = User.objects.get(username='admin')

    def test_api_correct_url(self):
        request = self.client.get('/robots_api/create_robot/')
        self.assertEqual(request.status_code, 200)

    def test_correct_data(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        data = {"model":"R2","version":"D2","created":"2022-12-31 23:59:59"}
        response = client.post('/robots_api/create_robot/', data=data, format='json')
        self.assertEqual(response.status_code, 201)
        assert Robot.objects.get(model='R2')

    def test_incorrect_data(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        data = {"model": "R2", "version": "D2"}
        response = client.post('/robots_api/create_robot/', data=data, format='json')
        self.assertEqual(response.status_code, 400)
        try:
            Robot.objects.get(model='R2')
        except ObjectDoesNotExist:
            assert True