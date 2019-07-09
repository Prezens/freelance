from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient, force_authenticate
from .models import Task

User = get_user_model()


class TaskModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='TestTest', password='123123', first_name='Test', last_name='Test', role='consumer')
        task = Task.objects.create(id=1, title='Create website', description='Shop', consumer=user, price=100)

    def test_title(self):
        t = Task.objects.get(id=1)
        field_title = t._meta.get_field('title').max_length
        self.assertEqual(field_title, 200)

    def test_consumer(self):
        t = Task.objects.get(id=1)
        self.assertNotEqual(t, None)


class TaskCreateUpdateDetail(APITestCase):
    def setUp(self):
        self.test_user_data = {
            'username': 'TestTest',
            'password': '123123',
            'first_name': 'Test',
            'last_name': 'Test',
            'email': 'test@test.te',
            'role': 'consumer',
            'balance': '0'
        }
        self.user = User.objects.create_user(**self.test_user_data)
        self.test_data = {
            'title': 'Create website',
            'description': 'Shop',
            'consumer': self.user,
            'price': 100
        }
    
    def test_create_task(self):
        client = APIClient()
        client.login(username=self.test_user_data['username'], password=self.test_user_data['password'])
        request = client.post('/task/create/', self.test_data)
        t = Task.objects.get(price=self.test_data['price'])
        self.assertEqual(str(t), self.test_data['title'])
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_update_task(self):
        test_user_data = {
            'username': 'executorrr',
            'password': '123123',
            'first_name': 'executor',
            'last_name': 'EXECUTOR',
            'email': 'executor@test.te',
            'role': 'executor',
            'balance': '0'
        }
        test_data = {
            'id': 1,
            'title': 'Create website',
            'description': 'Shop',
            'consumer': self.user,
            'price': 100
        }
        user = User.objects.create_user(**test_user_data)
        task = Task.objects.create(**test_data)

        client = APIClient()
        client.login(username=self.test_user_data['username'], password=self.test_user_data['password'])
        request = client.put('/task/' + str(test_data['id']) + '/update/', {'executor': user, 'done': True})
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
