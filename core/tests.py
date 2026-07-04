from django.test import TestCase
from django.urls import reverse

from .models import Category, Course, Enrollment, Lesson, Module, User


class SiteTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.instructor = User.objects.create_user(
            username="prof", password="pass12345", user_type="instructor"
        )
        cls.student = User.objects.create_user(
            username="etudiant", password="pass12345", user_type="student"
        )
        cls.category = Category.objects.create(name="Développement Web", icon="fa-code")
        cls.course = Course.objects.create(
            title="Cours Django",
            description="Apprendre Django.",
            short_description="Apprendre Django.",
            instructor=cls.instructor,
            category=cls.category,
            price=0,
            is_published=True,
        )
        module = Module.objects.create(course=cls.course, title="Intro", display_order=0)
        cls.lesson1 = Lesson.objects.create(
            module=module, title="Leçon 1", slug="lecon-1", display_order=0
        )
        cls.lesson2 = Lesson.objects.create(
            module=module, title="Leçon 2", slug="lecon-2", display_order=1
        )
        Course.objects.create(
            title="Brouillon",
            description="Non publié.",
            instructor=cls.instructor,
            category=cls.category,
            is_published=False,
        )

    def test_home_page(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cours Django")
        self.assertNotContains(response, "Brouillon")

    def test_course_list_and_search(self):
        response = self.client.get(reverse("course_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cours Django")

        response = self.client.get(reverse("course_list"), {"q": "introuvable-xyz"})
        self.assertContains(response, "Aucun cours trouvé")

        response = self.client.get(reverse("course_list"), {"category": self.category.slug})
        self.assertContains(response, "Cours Django")

    def test_category_list(self):
        response = self.client.get(reverse("category_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Développement Web")

    def test_course_detail(self):
        response = self.client.get(reverse("course_detail", args=[self.course.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cours Django")
        self.assertContains(response, "Leçon 1")

    def test_unpublished_course_returns_404(self):
        response = self.client.get(reverse("course_detail", args=["brouillon"]))
        self.assertEqual(response.status_code, 404)

    def test_enroll_requires_login(self):
        url = reverse("enroll_course", args=[self.course.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_enroll_and_viewer(self):
        self.client.login(username="etudiant", password="pass12345")
        response = self.client.get(reverse("enroll_course", args=[self.course.slug]))
        self.assertRedirects(response, reverse("course_viewer", args=[self.course.slug]))
        self.assertTrue(
            Enrollment.objects.filter(user=self.student, course=self.course).exists()
        )
        response = self.client.get(reverse("course_viewer", args=[self.course.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Leçon 1")

    def test_viewer_requires_enrollment(self):
        self.client.login(username="etudiant", password="pass12345")
        response = self.client.get(reverse("course_viewer", args=[self.course.slug]))
        self.assertRedirects(response, reverse("course_detail", args=[self.course.slug]))

    def test_complete_lessons_marks_course_completed(self):
        self.client.login(username="etudiant", password="pass12345")
        enrollment = Enrollment.objects.create(user=self.student, course=self.course)
        for lesson in (self.lesson1, self.lesson2):
            response = self.client.post(
                reverse("complete_lesson", args=[self.course.slug, lesson.slug])
            )
            self.assertEqual(response.status_code, 302)
        enrollment.refresh_from_db()
        self.assertTrue(enrollment.is_completed)
        self.assertTrue(hasattr(enrollment, "certificate"))
        self.student.refresh_from_db()
        self.assertEqual(self.student.completed_courses_count, 1)

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_shows_progress(self):
        self.client.login(username="etudiant", password="pass12345")
        Enrollment.objects.create(user=self.student, course=self.course)
        self.client.post(reverse("complete_lesson", args=[self.course.slug, self.lesson1.slug]))
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "50% complété")

    def test_register(self):
        response = self.client.post(reverse("register"), {
            "username": "nouveau",
            "email": "nouveau@example.com",
            "first_name": "Nouveau",
            "last_name": "Membre",
            "password1": "MotDePasse2026!",
            "password2": "MotDePasse2026!",
        })
        self.assertRedirects(response, reverse("dashboard"))
        self.assertTrue(User.objects.filter(username="nouveau").exists())

    def test_login_and_logout(self):
        response = self.client.post(reverse("login"), {
            "username": "etudiant",
            "password": "pass12345",
        })
        self.assertRedirects(response, reverse("dashboard"))
        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, reverse("home"))

    def test_api_courses(self):
        response = self.client.get("/api/courses/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["title"], "Cours Django")

    def test_api_categories(self):
        response = self.client.get("/api/categories/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)
