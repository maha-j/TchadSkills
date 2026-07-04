from rest_framework import viewsets

from .models import Category, Course
from .serializers import CategorySerializer, CourseSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    lookup_field = "slug"


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        Course.objects.filter(is_published=True)
        .select_related("instructor", "category")
        .order_by("-created_at")
    )
    serializer_class = CourseSerializer
    lookup_field = "slug"
    search_fields = ("title", "description")
