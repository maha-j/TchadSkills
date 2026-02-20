from rest_framework import viewsets, mixins
from .models import Course, Category, Lesson
from .serializers import CourseSerializer, CategorySerializer, LessonSerializer

class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.select_related('category').all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        # Implement filtering logic if needed
        return queryset

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.prefetch_related('courses').all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        # Implement filtering logic if needed
        return queryset

class LessonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Lesson.objects.select_related('course').all()
    serializer_class = LessonSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        # Implement filtering logic if needed
        return queryset

# Keeping the home template view as it is
