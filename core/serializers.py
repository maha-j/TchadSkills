from rest_framework import serializers

from .models import Category, Course


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug", "description", "icon")


class CourseSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name", default="", read_only=True)
    instructor = serializers.CharField(source="instructor.get_full_name", read_only=True)
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            "id", "title", "slug", "short_description", "description",
            "category", "instructor", "thumbnail", "level", "price",
        )

    def get_thumbnail(self, obj):
        if obj.thumbnail:
            request = self.context.get("request")
            url = obj.thumbnail.url
            return request.build_absolute_uri(url) if request else url
        return None
