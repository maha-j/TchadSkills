from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.api_views import CourseViewSet, CategoryViewSet

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),  # for authentication
    # Include any existing home view and static file serving here
]