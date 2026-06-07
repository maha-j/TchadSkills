from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Category, Course


class UserModelTest(TestCase):
	def test_create_user_defaults(self):
		User = get_user_model()
		user = User.objects.create_user(username='testuser', email='t@example.com', password='secret123')
		self.assertEqual(user.user_type, 'student')
		self.assertTrue(user.check_password('secret123'))


class CourseModelTest(TestCase):
	def test_course_slug_auto_populated(self):
		User = get_user_model()
		instructor = User.objects.create_user(username='inst', password='secret123')
		category = Category.objects.create(name='Python')
		course = Course.objects.create(title='Intro to Python', description='desc', instructor=instructor, category=category)
		self.assertIsNotNone(course.slug)
		self.assertEqual(course.slug, 'intro-to-python')
