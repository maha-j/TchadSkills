from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Category, Course, Lesson, VerificationCode
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    SendVerificationCodeSerializer,
    CategorySerializer,
    CourseSerializer,
    LessonSerializer,
)


def home(request):
    return render(request, 'index.html')


def login_page(request):
    return render(request, 'login.html')


def register_page(request):
    return render(request, 'register.html')


def logout_page(request):
    return render(request, 'logout.html')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        # Inscription (POST) ouverte à tous — lecture/modif nécessite auth
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(pk=response.data['id'])
        refresh = RefreshToken.for_user(user)
        response.data['access'] = str(refresh.access_token)
        response.data['refresh'] = str(refresh)
        return response


class SendVerificationCodeView(generics.GenericAPIView):
    serializer_class = SendVerificationCodeSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contact = serializer.validated_data['contact']

        verification = VerificationCode.create_code(contact)

        if '@' in contact:
            send_mail(
                subject='Votre code de vérification TchadSkills',
                message=f'Votre code de vérification est : {verification.code}',
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@tchadskills.td'),
                recipient_list=[contact],
                fail_silently=True,
            )
        else:
            # Pour les tests et le développement sans service SMS,
            # le code est stocké en base. En production, connectez une API SMS ici.
            print(f"Vérification SMS envoyé à {contact} : {verification.code}")

        return Response({'detail': 'Code de vérification envoyé.'}, status=status.HTTP_200_OK)


class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.filter(is_published=True)
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]
