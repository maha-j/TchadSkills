from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model

from .models import Category, Course


class CoreAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        User = get_user_model()
        self.user = User.objects.create_user(username='apiuser', password='secret123')
        self.category = Category.objects.create(name='Data')
        self.course = Course.objects.create(title='Public Course', description='desc', instructor=self.user, category=self.category, is_published=True)

    def test_categories_list(self):
        resp = self.client.get('/api/categories/')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(any(item.get('name') == 'Data' for item in data))

    def test_courses_list_public(self):
        resp = self.client.get('/api/courses/')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(any(item.get('title') == 'Public Course' for item in data))

    def test_user_create(self):
        data = {'username': 'newuser', 'email': 'n@example.com', 'password': 'newpass123'}
        resp = self.client.post('/api/users/', data)
        self.assertIn(resp.status_code, (200, 201))
        User = get_user_model()
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_token_obtain(self):
        resp = self.client.post('/api/token/', {'username': 'apiuser', 'password': 'secret123'})
        self.assertEqual(resp.status_code, 200)
        self.assertIn('access', resp.json())
