import os
import django
import random

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tchadskills_project.settings')
django.setup()

from core.models import User, Category, Course, Lesson
from django.utils.text import slugify

def seed():
    print("🚀 Début du peuplement de la base de données TchadSkills...")

    # 1. Création d'un super-utilisateur admin
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@tchadskills.td', 'admin123', user_type='admin')
        print("✅ Compte administrateur créé (admin / admin123)")

    # 2. Création d'un instructeur de démo
    instructor, created = User.objects.get_or_create(
        username='ahmed_pro',
        defaults={
            'email': 'ahmed@tchadskills.td',
            'first_name': 'Ahmed',
            'last_name': 'Mahamat',
            'user_type': 'instructor',
            'bio': 'Expert en développement web avec 10 ans d\'expérience au Tchad.'
        }
    )
    if created:
        instructor.set_password('ahmed123')
        instructor.save()
        print(f"✅ Instructeur {instructor.username} créé.")

    # 3. Création des catégories
    categories_data = [
        {'name': 'Développement Web', 'icon': 'fa-code', 'description': 'Apprenez à créer des sites et applications modernes.'},
        {'name': 'Marketing Digital', 'icon': 'fa-bullhorn', 'description': 'Maîtrisez les réseaux sociaux et le SEO.'},
        {'name': 'Bureautique', 'icon': 'fa-file-excel', 'description': 'Devenez expert sur Excel, Word et PowerPoint.'},
        {'name': 'Entrepreneuriat', 'icon': 'fa-lightbulb', 'description': 'Lancez votre startup au Tchad avec succès.'},
    ]

    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={
                'icon': cat_data['icon'],
                'description': cat_data['description'],
                'is_active': True
            }
        )
        if created:
            print(f"✅ Catégorie '{category.name}' créée.")

    # 4. Création de quelques cours de démo
    courses_data = [
        {
            'title': 'Maîtriser Python de A à Z',
            'category_name': 'Développement Web',
            'description': 'Le langage le plus populaire pour le data science et le web.',
            'level': 'beginner',
            'price': 15000
        },
        {
            'title': 'Marketing Facebook pour PME Tchadiennes',
            'category_name': 'Marketing Digital',
            'description': 'Boostez vos ventes locales grâce à la publicité Facebook.',
            'level': 'intermediate',
            'price': 10000
        },
        {
            'title': 'Excel Avancé pour la Gestion',
            'category_name': 'Bureautique',
            'description': 'Tableaux croisés dynamiques et automatisation pour les pros.',
            'level': 'advanced',
            'price': 12000
        }
    ]

    for c_data in courses_data:
        category = Category.objects.get(name=c_data['category_name'])
        course, created = Course.objects.get_or_create(
            title=c_data['title'],
            defaults={
                'instructor': instructor,
                'category': category,
                'description': c_data['description'],
                'level': c_data['level'],
                'price': c_data['price'],
                'is_published': True
            }
        )
        if created:
            print(f"✅ Cours '{course.title}' créé.")
            
            # Ajouter des leçons de démo pour chaque cours
            for i in range(1, 4):
                Lesson.objects.create(
                    course=course,
                    title=f"Leçon {i}: Introduction à {course.title}",
                    content="Contenu de la leçon en cours de préparation...",
                    display_order=i
                )
            print(f"   📚 3 leçons ajoutées au cours '{course.title}'.")

    print("\n✨ Base de données TchadSkills prête et professionnelle !")

if __name__ == '__main__':
    seed()
