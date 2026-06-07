from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Category, Course, Lesson
from .serializers import CourseSerializer


class CourseSerializerTest(TestCase):
    def test_serializer_contains_expected_fields(self):
        User = get_user_model()
        instructor = User.objects.create_user(username='inst', password='secret123', first_name='Inst', last_name='Ructor')
        category = Category.objects.create(name='Python')
        course = Course.objects.create(title='Intro to Python', description='desc', instructor=instructor, category=category, is_published=True)
        lesson = Lesson.objects.create(course=course, title='Lesson 1', content='content')
        serializer = CourseSerializer(course)
        data = serializer.data
        self.assertEqual(data['instructor_name'], instructor.get_full_name())
        self.assertEqual(data['category_name'], category.name)
        self.assertIsInstance(data['lessons'], list)
        self.assertEqual(data['lessons'][0]['title'], 'Lesson 1')
