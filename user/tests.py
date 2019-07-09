from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIClient, force_authenticate, APIRequestFactory
from .models import User


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='TestTest', password='123123', first_name='Test', last_name='Test', role='consumer')

    def test_username(self):
        user = User.objects.get(id=1)
        field_username = user._meta.get_field('username').max_length
        self.assertEqual(field_username, 150)

    def test_len_password(self):
        user = User.objects.get(id=1)
        field_password = user.password
        self.assertGreaterEqual(len(field_password), 6)

    def test_role(self):
        user = User.objects.get(id=1)
        field_role = user.role
        self.assertIn(field_role, ['consumer', 'executor'])


class UserRegisterAndLoginTest(APITestCase):
    def setUp(self):
        self.test_data = {
            'username': 'TestTest',
            'password': '123123',
            'first_name': 'Test',
            'last_name': 'Test',
            'email': 'test@test.te',
            'role': 'consumer',
            'balance': '0'
        }

    def test_register(self):
        client = APIClient()
        request = client.post('/register/', self.test_data)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        user = User.objects.create_user(**self.test_data)
        
        client = APIClient()
        # request = client.get('/login/')
        s = client.login(username=self.test_data['username'], password=self.test_data['password'])
        self.assertEqual(s, True)
