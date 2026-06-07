from django.utils import timezone
from rest_framework import serializers
from .models import User, Category, Course, Lesson, VerificationCode


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, min_length=8)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'user_type', 'phone', 'avatar', 'bio', 'password')
        read_only_fields = ('id',)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class SendVerificationCodeSerializer(serializers.Serializer):
    contact = serializers.CharField(required=True, max_length=255)

    def validate_contact(self, value):
        if '@' in value:
            return serializers.EmailField().run_validation(value)
        return value

    def validate(self, data):
        contact = data['contact']
        if User.objects.filter(email=contact).exists() or User.objects.filter(phone=contact).exists():
            raise serializers.ValidationError('Ce contact est déjà utilisé. Veuillez vous connecter ou choisir un autre contact.')
        return data


class RegisterSerializer(UserSerializer):
    verification_code = serializers.CharField(write_only=True, required=True, max_length=6)
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('verification_code',)
        read_only_fields = UserSerializer.Meta.read_only_fields

    def validate(self, data):
        contact = data.get('email') or data.get('phone')
        if not contact:
            raise serializers.ValidationError('Un email ou un numéro de téléphone est requis pour l’inscription.')

        code = data.get('verification_code')
        if not code:
            raise serializers.ValidationError('Le code de vérification est requis.')

        verification = VerificationCode.objects.filter(
            contact=contact,
            code=code,
            purpose='registration',
            is_used=False,
            expires_at__gt=timezone.now()
        ).order_by('-created_at').first()
        if not verification:
            raise serializers.ValidationError('Le code de vérification est invalide ou expiré.')

        data['verification_record'] = verification
        return data

    def create(self, validated_data):
        validated_data.pop('verification_code', None)
        verification = validated_data.pop('verification_record', None)
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        if verification:
            verification.is_used = True
            verification.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            if attr == 'verification_code':
                continue
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    instructor_name = serializers.ReadOnlyField(source='instructor.get_full_name')
    category_name = serializers.ReadOnlyField(source='category.name')
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
