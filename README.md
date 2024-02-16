# REST API YaMDb
## Описание
В проекте реализован REST API YaMDb: платформы для сбора отзывов пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.  
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).  
Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).  
Добавлять произведения, категории и жанры может только администратор.  
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.
Пользователи могут оставлять комментарии к отзывам.  
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

## Команда разработки проекта

Владимир Матасов (тимлид) - реализация Auth/Users  
ссылка на github: https://github.com/Anquientas/

Елена Альтман - реализация Categories/Genres/Titles  
ссылка на github: https://github.com/altmanhellen/

Павел Гусев - реализация Review/Comments  
ссылка на github: https://github.com/Pavel950/

## Стек проекта
Python, Django, Django REST framework, SQLite  
Используемые библиотеки и пакеты сохранены в файле requirements.txt

## Как запустить проект

**Клонировать репозиторий и перейти в него в командной строке:**

```
git clone https://github.com/Anquientas/api_yamdb.git
```

```
cd api_yamdb
```

**Cоздать и активировать виртуальное окружение (рекомендуется использовать Python 3.9):**

* для Linux:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

* для Windows:

```
py -3.9 -m venv venv
```

```
source venv/Scripts/activate
```

**Установить зависимости из файла requirements.txt:**

* для Linux:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

* для Windows:

```
py -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

**Выполнить миграции:**

* для Linux:

```
python3 manage.py migrate
```

* для Windows:

```
py manage.py migrate
```

**Наполнить базу данных с помощью импорта из csv-файлов:**

Инструкции по Импорту Данных

Для импорта данных в базу данных используйте следующие функции. Каждая функция отвечает за импорт определенного типа данных из CSV-файлов.

import_users: Импорт пользователей из файла 'static/data/users.csv'. Функция проверяет, существует ли пользователь с таким же email, и если нет, создает нового пользователя с данными из файла.  
import_category: Импорт категорий из файла 'static/data/category.csv'. Если категория с таким же slug еще не существует, она будет создана.  
import_genre: Импорт жанров из файла 'static/data/genre.csv'. Если жанр с таким же slug еще не существует, он будет создан.  
import_title: Импорт произведений из файла 'static/data/titles.csv'. Создает новое произведение с указанными в файле параметрами.  
import_review: Импорт отзывов из файла 'static/data/review.csv'. Создает отзывы на основе данных из файла.  
import_genretitle: Создание связей между жанрами и произведениями. Для каждой записи в файле 'static/data/genre_title.csv' создается связь между жанром и произведением.  
import_comment: Импорт комментариев из файла 'static/data/comments.csv'. Создает комментарии на основе данных из файла.  
Запустите shell

```
python manage.py shell
```
Импортируйте функции

```
from import_data import import_users, import_category, import_genre, import_title, import_genretitle, import_review, import_comment
```
Запустите функции

```
import_users()
import_category()
import_genre()
import_title()
import_genretitle()
import_review()
import_comment()
```

**Запустить проект:**

* для Linux:

```
python3 manage.py runserver
```

* для Windows:

```
py manage.py runserver
```

## Документация

Когда вы запустите проект, по адресу http://127.0.0.1:8000/redoc/ будет доступна документация для API YaMDb.

## Примеры запросов

### Получение информации о произведении:

**запрос:**
```
GET .../api/v1/titles/2/
```

**ответ:**
```
{
  "id": 2,
  "name": "Винни-Пух",
  "year": 1926,
  "rating": 8,
  "description": "Детская повесть Алана Милна",
  "genre": [
    {
      "name": "Детская повесть",
      "slug": "child-story"
    }
  ],
  "category": {
    "name": "Книга",
    "slug": "book"
  }
}
```

### Добавление комментария к отзыву:

**запрос:**
```
POST .../api/v1/titles/3/reviews/1/comments/
```

**тело запроса:**
```
{
"text": "Поддерживаю предыдущего оратора!"
}
```

**ответ:**
```
{
"id": 5,
"text": "Поддерживаю предыдущего оратора!",
"author": "Vasya",
"pub_date": "2024-02-02T14:15:22Z"
}
```

Более подробную информацию о запросах и возможных параметрах см. в документации.


