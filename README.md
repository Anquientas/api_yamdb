# REST API YaTube
## Описание
В проекте реализован REST API YaMdb: платформы 

Проект выполнен на языке Python 3.9 с использованием Django Rest Framework

Используемые библиотеки и пакеты сохранены в файле requirements.txt

Документацию проекта можно изучить после запуска проекта по адресу:

```
http://127.0.0.1:8000/redoc/
```

## Как запустить проект

**Клонировать репозиторий и перейти в него в командной строке:**

```
git clone https://github.com/Anquientas/*
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

**Запустить проект:**

* для Linux:

```
python3 manage.py runserver
```

* для Windows:

```
py manage.py runserver
```

## Примеры запросов

Для получения * необходимо выполнить запрос по адресу:
```
http://*/api/v1/
```

Пример успешного ответа в формате JSON:

```

```

