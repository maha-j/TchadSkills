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

    def test_register_returns_tokens(self):
        data = {'username': 'newuser2', 'email': 'n2@example.com', 'password': 'newpass123'}
        resp = self.client.post('/api/register/', data)
        self.assertEqual(resp.status_code, 201)
        json_data = resp.json()
        self.assertIn('access', json_data)
        self.assertIn('refresh', json_data)
        User = get_user_model()
        self.assertTrue(User.objects.filter(username='newuser2').exists())

    def test_token_obtain(self):
        resp = self.client.post('/api/login/', {'username': 'apiuser', 'password': 'secret123'})
        self.assertEqual(resp.status_code, 200)
        self.assertIn('access', resp.json())
        self.assertIn('refresh', resp.json())

    def test_me_authenticated(self):
        resp = self.client.post('/api/login/', {'username': 'apiuser', 'password': 'secret123'})
        self.assertEqual(resp.status_code, 200)
        access_token = resp.json()['access']
        auth_client = APIClient()
        auth_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        me_resp = auth_client.get('/api/me/')
        self.assertEqual(me_resp.status_code, 200)
        self.assertEqual(me_resp.json()['username'], 'apiuser')

    def test_me_patch_updates_profile(self):
        resp = self.client.post('/api/login/', {'username': 'apiuser', 'password': 'secret123'})
        self.assertEqual(resp.status_code, 200)
        access_token = resp.json()['access']
        auth_client = APIClient()
        auth_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        patch_resp = auth_client.patch('/api/me/', {'first_name': 'API', 'last_name': 'User'})
        self.assertEqual(patch_resp.status_code, 200)
        self.assertEqual(patch_resp.json()['first_name'], 'API')
        self.assertEqual(patch_resp.json()['last_name'], 'User')

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'API')
        self.assertEqual(self.user.last_name, 'User')
