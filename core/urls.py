from django.contrib.auth import views as auth_views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import api, views

router = DefaultRouter()
router.register("courses", api.CourseViewSet, basename="api-course")
router.register("categories", api.CategoryViewSet, basename="api-category")

urlpatterns = [
    path("", views.home, name="home"),
    path("courses/", views.course_list, name="course_list"),
    path("categories/", views.category_list, name="category_list"),
    path("course/<slug:slug>/", views.course_detail, name="course_detail"),
    path("course/<slug:slug>/enroll/", views.enroll_course, name="enroll_course"),
    path("course/<slug:slug>/learn/", views.course_viewer, name="course_viewer"),
    path(
        "course/<slug:slug>/lesson/<slug:lesson_slug>/complete/",
        views.complete_lesson,
        name="complete_lesson",
    ),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("register/", views.register, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="login.html", redirect_authenticated_user=True),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("api/", include(router.urls)),
]
