from rest_framework.test import APITestCase


class TestAPIPost(APITestCase):

    def test_api_correct_url(self):
        request = self.client.get('/robots_api/create_robot/')
        self.assertEqual(request.status_code, 200)