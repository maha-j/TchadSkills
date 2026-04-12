from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category, Course, Module, Lesson, Enrollment, LessonProgress, Certificate

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "user_type",
        "is_staff",
    )
    list_filter = ("user_type", "is_staff", "is_superuser")
    fieldsets = UserAdmin.fieldsets + (
        (
            "Informations TchadSkills",
            {
                "fields": (
                    "user_type",
                    "phone",
                    "avatar",
                    "bio",
                    "total_learning_hours",
                    "completed_courses_count",
                )
            },
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Informations TchadSkills", {"fields": ("user_type", "phone", "email")}),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "display_order")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("is_active", "display_order")
    search_fields = ("name",)


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


class ModuleInline(admin.StackedInline):
    model = Module
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "instructor", "category", "level", "price", "is_published")
    list_filter = ("is_published", "level", "category")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "description")
    inlines = [ModuleInline]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "display_order")
    list_filter = ("course",)
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "module", "display_order", "is_preview")
    list_filter = ("module__course", "module")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "enrolled_at", "is_completed")
    list_filter = ("is_completed", "course")
    search_fields = ("user__username", "course__title")


admin.site.register(LessonProgress)
admin.site.register(Certificate)

# Personnalisation de l'interface d'administration
admin.site.site_header = "Administration TchadSkills"
admin.site.site_title = "Portail Admin TchadSkills"
admin.site.index_title = "Bienvenue dans la gestion de TchadSkills"
