import os
import django
import random
from decimal import Decimal
from django.utils.text import slugify

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tchadskills_project.settings')
django.setup()

from core.models import User, Category, Course, Module, Lesson, Enrollment

def seed_data():
    print("🚀 Début de l'upgrade des données...")

    # 1. Création des utilisateurs
    admin, _ = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@tchadskills.td',
            'user_type': 'admin',
            'is_staff': True,
            'is_superuser': True
        }
    )
    admin.set_password('admin123')
    admin.save()

    instructor, _ = User.objects.get_or_create(
        username='mahadi',
        defaults={
            'email': 'mahadi@tchadskills.td',
            'user_type': 'instructor',
            'first_name': 'Mahadi',
            'last_name': 'Abderaman',
            'bio': 'Expert en développement Web et formateur passionné au Tchad.'
        }
    )
    instructor.set_password('instructor123')
    instructor.save()

    # 2. Création des catégories
    categories_data = [
        {'name': 'Développement Web', 'icon': 'fa-code', 'desc': 'Apprenez à créer des sites et applications modernes.'},
        {'name': 'Marketing Digital', 'icon': 'fa-bullhorn', 'desc': 'Maîtrisez les réseaux sociaux et la publicité en ligne.'},
        {'name': 'Bureautique', 'icon': 'fa-file-excel', 'desc': 'Devenez un expert sur Excel, Word et PowerPoint.'},
        {'name': 'Entrepreneuriat', 'icon': 'fa-lightbulb', 'desc': 'Lancez et gérez votre propre entreprise au Tchad.'},
    ]

    categories = []
    for cat_data in categories_data:
        cat, _ = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={
                'icon': cat_data['icon'],
                'description': cat_data['desc']
            }
        )
        categories.append(cat)

    # 3. Création des cours
    courses_data = [
        {
            'title': 'Maîtriser Python & Django',
            'cat': categories[0],
            'price': 25000,
            'level': 'beginner',
            'desc': 'Devenez un développeur web complet en apprenant le langage Python et le framework Django.'
        },
        {
            'title': 'Excel pour les Professionnels',
            'cat': categories[2],
            'price': 15000,
            'level': 'intermediate',
            'desc': 'Optimisez votre productivité au bureau avec les fonctions avancées de Microsoft Excel.'
        },
        {
            'title': 'Lancer sa Startup au Tchad',
            'cat': categories[3],
            'price': 0,
            'level': 'beginner',
            'desc': 'Un guide complet pour transformer votre idée en entreprise florissante dans le contexte tchadien.'
        }
    ]

    for c_data in courses_data:
        course, created = Course.objects.get_or_create(
            title=c_data['title'],
            defaults={
                'instructor': instructor,
                'category': c_data['cat'],
                'price': Decimal(c_data['price']),
                'level': c_data['level'],
                'description': c_data['desc'],
                'short_description': c_data['desc'][:100] + '...',
                'is_published': True
            }
        )

        if created:
            # 4. Création des modules et leçons pour chaque cours
            modules_titles = ['Introduction', 'Les Fondamentaux', 'Projet Pratique', 'Conclusion']
            for i, m_title in enumerate(modules_titles):
                module = Module.objects.create(
                    course=course,
                    title=m_title,
                    display_order=i
                )
                
                # Création de 2-3 leçons par module
                for j in range(1, 4):
                    lesson_title = f"Leçon {j}: {m_title} - Partie {j}"
                    # Utilisation du slug unique incluant l'ID du cours pour éviter les collisions
                    Lesson.objects.create(
                        module=module,
                        title=lesson_title,
                        slug=slugify(f"{course.id}-{lesson_title}"),
                        content=f"Ceci est le contenu détaillé de la leçon {j} du module {m_title} pour le cours {course.title}.",
                        duration_minutes=random.randint(5, 20),
                        display_order=j
                    )

    print("✅ Upgrade des données terminé avec succès !")

if __name__ == '__main__':
    seed_data()
