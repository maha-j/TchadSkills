from django.shortcuts import render
from .models import Course, Category

def home(request):
    courses = Course.objects.filter(is_published=True)[:6]
    categories = Category.objects.filter(is_active=True)
    return render(request, 'index.html', {
        'courses': courses,
        'categories': categories
    })
