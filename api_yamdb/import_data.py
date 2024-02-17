import os
import django
import csv


def import_users():
    with open('static/data/users.csv',
              newline='',
              encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if User.objects.filter(email=row['email']).exists():
                print(f"Пользователь с email {row['email']} уже существует")
                continue
            User.objects.create(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                role=row['role'],
                bio=row.get('bio',),
                first_name=row.get('first_name',),
                last_name=row.get('last_name',)
            )


def import_category():
    with open('static/data/category.csv',
              newline='',
              encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            slug = row['slug']
            if not Category.objects.filter(slug=slug).exists():
                Category.objects.create(name=row['name'], slug=slug)


def import_genre():
    with open('static/data/genre.csv',
              newline='',
              encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            slug = row['slug']
            if not Genre.objects.filter(slug=slug).exists():
                Genre.objects.create(name=row['name'], slug=slug)


def import_title():
    with open('static/data/titles.csv',
              newline='',
              encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            category, _ = Category.objects.get_or_create(id=row['category'])
            Title.objects.create(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category=category
            )


def import_review():
    with open('static/data/review.csv',
              newline='',
              encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            author = User.objects.get(id=row['author'])
            title = Title.objects.get(id=row['title_id'])
            Review.objects.create(
                id=row['id'],
                text=row['text'],
                author=author,
                score=row['score'],
                pub_date=row['pub_date'],
                title=title
            )


def import_genretitle():
    with open('static/data/genre_title.csv',
              newline='',
              encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if not Title.objects.filter(id=row['title_id']).exists():
                print(f"Произведение с ID {row['title_id']} не найдено")
                continue
            title = Title.objects.get(id=row['title_id'])
            genre = Genre.objects.get(id=row['genre_id'])
            title.genre.add(genre)


def import_comment():
    with open('static/data/comments.csv',
              newline='',
              encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            author = User.objects.get(id=row['author'])
            review = Review.objects.get(id=row['review_id'])
            if not Review.objects.filter(id=row['review_id']).exists():
                print(f"Ревью с ID {row['review_id']} не найдено")
                continue
            Comment.objects.create(
                id=row['id'],
                review=review,
                text=row['text'],
                author=author,
                pub_date=row['pub_date']
            )


def main():
    import_users()
    import_category()
    import_genre()
    import_title()
    import_genretitle()
    import_review()
    import_comment()


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_yamdb.settings')
    django.setup()
    try:
        from reviews.models import (
            Category,
            Comment,
            Genre,
            Title,
            Review,
            User
        )
        main()
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
