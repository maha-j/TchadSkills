from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from core.views import (
    home,
    login_page,
    register_page,
    logout_page,
    UserViewSet,
    CategoryViewSet,
    CourseViewSet,
    LessonViewSet,
    RegisterView,
    SendVerificationCodeView,
    MeView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'lessons', LessonViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', login_page, name='login_page'),
    path('register/', register_page, name='register_page'),
    path('logout/', logout_page, name='logout_page'),
    path('api/', include(router.urls)),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/send-code/', SendVerificationCodeView.as_view(), name='send_verification_code'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/me/', MeView.as_view(), name='me'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
