import uuid

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Prefetch, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import RegisterForm
from .models import Category, Certificate, Course, Enrollment, Lesson, LessonProgress


def _published_courses():
    return (
        Course.objects.filter(is_published=True)
        .select_related("instructor", "category")
    )


def home(request):
    courses = _published_courses().order_by("-created_at")[:6]
    categories = Category.objects.filter(is_active=True)
    return render(request, "home.html", {
        "courses": courses,
        "categories": categories,
    })


def course_list(request):
    courses = _published_courses().order_by("-created_at")
    categories = Category.objects.filter(is_active=True)

    query = request.GET.get("q", "").strip()
    if query:
        courses = courses.filter(
            Q(title__icontains=query)
            | Q(short_description__icontains=query)
            | Q(description__icontains=query)
        )

    current_category = request.GET.get("category", "").strip()
    if current_category:
        courses = courses.filter(category__slug=current_category)

    return render(request, "course_list.html", {
        "courses": courses,
        "categories": categories,
        "query": query,
        "current_category": current_category,
    })


def category_list(request):
    categories = (
        Category.objects.filter(is_active=True)
        .annotate(course_count=Count("courses", filter=Q(courses__is_published=True)))
    )
    return render(request, "category_list.html", {"categories": categories})


def course_detail(request, slug):
    course = get_object_or_404(
        _published_courses().prefetch_related(
            Prefetch("modules__lessons", queryset=Lesson.objects.order_by("display_order"))
        ),
        slug=slug,
    )
    is_enrolled = (
        request.user.is_authenticated
        and Enrollment.objects.filter(user=request.user, course=course).exists()
    )
    return render(request, "course_detail.html", {
        "course": course,
        "modules": course.modules.all(),
        "is_enrolled": is_enrolled,
    })


@login_required
def enroll_course(request, slug):
    course = get_object_or_404(_published_courses(), slug=slug)
    _, created = Enrollment.objects.get_or_create(user=request.user, course=course)
    if created:
        messages.success(request, f"Vous êtes maintenant inscrit au cours « {course.title} ».")
    else:
        messages.info(request, "Vous êtes déjà inscrit à ce cours.")
    return redirect("course_viewer", slug=course.slug)


def _course_progress(enrollment):
    total = Lesson.objects.filter(module__course=enrollment.course).count()
    if total == 0:
        return 0
    completed = enrollment.lesson_progress.filter(is_completed=True).count()
    return round(completed * 100 / total)


@login_required
def course_viewer(request, slug):
    course = get_object_or_404(
        _published_courses().prefetch_related(
            Prefetch("modules__lessons", queryset=Lesson.objects.order_by("display_order"))
        ),
        slug=slug,
    )
    enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
    if enrollment is None:
        messages.warning(request, "Inscrivez-vous d'abord à ce cours pour y accéder.")
        return redirect("course_detail", slug=course.slug)

    lessons = Lesson.objects.filter(module__course=course).order_by(
        "module__display_order", "display_order"
    )

    lesson_slug = request.GET.get("lesson")
    current_lesson = None
    if lesson_slug:
        current_lesson = lessons.filter(slug=lesson_slug).first()
    if current_lesson is None:
        current_lesson = lessons.first()

    completed_ids = set(
        enrollment.lesson_progress.filter(is_completed=True).values_list("lesson_id", flat=True)
    )

    next_lesson = None
    if current_lesson:
        lesson_list = list(lessons)
        idx = lesson_list.index(current_lesson)
        if idx + 1 < len(lesson_list):
            next_lesson = lesson_list[idx + 1]

    return render(request, "course_viewer.html", {
        "course": course,
        "modules": course.modules.all(),
        "current_lesson": current_lesson,
        "next_lesson": next_lesson,
        "completed_ids": completed_ids,
        "progress_percent": _course_progress(enrollment),
        "is_current_completed": current_lesson is not None and current_lesson.id in completed_ids,
    })


@require_POST
@login_required
def complete_lesson(request, slug, lesson_slug):
    course = get_object_or_404(_published_courses(), slug=slug)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
    lesson = get_object_or_404(Lesson, slug=lesson_slug, module__course=course)

    progress, _ = LessonProgress.objects.get_or_create(enrollment=enrollment, lesson=lesson)
    if not progress.is_completed:
        progress.is_completed = True
        progress.save(update_fields=["is_completed"])

    total = Lesson.objects.filter(module__course=course).count()
    completed = enrollment.lesson_progress.filter(is_completed=True).count()
    if total > 0 and completed >= total and not enrollment.is_completed:
        enrollment.is_completed = True
        enrollment.completed_at = timezone.now()
        enrollment.save(update_fields=["is_completed", "completed_at"])
        request.user.completed_courses_count = Enrollment.objects.filter(
            user=request.user, is_completed=True
        ).count()
        request.user.save(update_fields=["completed_courses_count"])
        Certificate.objects.get_or_create(
            enrollment=enrollment,
            defaults={"certificate_id": f"TS-{uuid.uuid4().hex[:10].upper()}"},
        )
        messages.success(request, f"Félicitations ! Vous avez terminé le cours « {course.title} ». 🎉")

    next_url = request.POST.get("next")
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)
    return redirect("course_viewer", slug=course.slug)


@login_required
def dashboard(request):
    enrollments = (
        Enrollment.objects.filter(user=request.user)
        .select_related("course__instructor", "course__category")
        .order_by("-enrolled_at")
    )
    for enrollment in enrollments:
        enrollment.progress_percent = _course_progress(enrollment)
    return render(request, "dashboard.html", {"enrollments": enrollments})


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Bienvenue sur TchadSkills, {user.get_full_name()} !")
            return redirect("dashboard")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})
