# Методические указания по выполнению лабораторной работы №2  

## Обращение к БД из Python

В этой части лабораторной работы необходимо создать подключение из
Python к PostgreSQL, занести и выбрать несколько записей с помощью кода.

Для начала требуется установить пакет psycopg2-binary из pip. Это необходимый
набор классов и функций для работы с postgresql из вашего кода.

Команда для установки: `pip install psycopg2-binary`

В этой части вашей задачей является написание простого скрипта, который
подключается к базе данных, добавляет одну запись, затем получает и выводит
на экран все записи таблицы books, а затем удаляет все записи.

`Пример`

```python
import psycopg2

conn = psycopg2.connect(dbname="postgres", host="192.168.0.189", user="student", password="root", port="5432")

cursor = conn.cursor()
 
cursor.execute("INSERT INTO public.books (id, name, description) VALUES(1, 'Мастер и Маргарита', 'Крутая книга')")
 
conn.commit()   # реальное выполнение команд sql1
 
cursor.close()
conn.close()
```

`Итог`

![Создание проекта](assets/12.png)

## Django ORM

Django предоставляет удобные возможности для представления базы
данных в виде python-объектов. Django ORM
облегчает и ускоряет разработку. Однако необходимо помнить, что в случае
реализации сложных SQL-запросов бывает быстрее и выгоднее использовать
чистые запросы без ORM.

Для использования ORM требуется описать свои модели предметной
области в виде классов, наследованных от django.db.models.Model.

Примеры работы с ORM:
https://django.fun/docs/django/ru/3.2/topics/db/models/

Чтобы методы модели работали, необходимо указать настройки
подключения БД в `settings.py`

`settings.py`
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'first_db',
        'USER': 'dbuser',
        'PASSWORD': '123',
        'HOST': 'localhost',
        'PORT': 5432, # Стандартный порт PostgreSQL
        'OPTIONS': {'charset': 'utf8'},
        'TEST_CHARSET': 'utf8',
    }
}
```

В этой части лабораторной работы требуется самостоятельно создать
модели по предметной области из предыдущей лабораторной работы.

Вы можете создать классы моделей всех таблиц в вашей БД с помощью

```
python manage.py inspectdb
```

Все запросы к БД представляются в Django ORM в виде объектов QuerySet.
Это своеобразный “конструктор” запросов, который позволяет с помощью кода
“собрать” SQL-запрос. Примеры работы с queryset и моделями можно найти
здесь: https://django.fun/docs/django/ru/3.2/topics/db/queries/

Кроме возможности создать модели и управлять ими из кода, Django ORM
также позволяет создавать БД по описанию моделей, а также изменять
структуру БД при изменении моделей.

Для этих действий используются так называемые миграции. Это скрипты,
которыу выполняют преобразование схемы базы данных с помощью ALTER
TABLE.

Миграции в Django создаются с помощью команды `manage.py
makemigrations <название приложения>`. После того, как миграция создана
(скрипт миграции создался и добавился в папку migrations), ее нужно применить
с помощью команды `manage.py migrate <название приложения>`.

Все изменения моделей (или их создание) будут фиксироваться в
миграции. Если модели до миграции не было, значит после применения
миграции будет создана соответствующая таблица. Если модель изменена
(например, добавлено поле), после применения миграции это поле будет
добавлено в соответствующую таблицу.

`Пример`

`models.py`
```python
from django.db import models

# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'books'
```

`urls.py`
```python
    path('', views.bookList),
    path('book/<int:id>/', views.GetBook, name='book_url')
```

`views.py`
```python
from bmstu_lab.models import Book

def bookList(request):
    return render(request, 'books.html', {'data' : {
        'current_date': date.today(),
        'books': Book.objects.all()
    }})

def GetBook(request, id):
    return render(request, 'book.html', {'data' : {
        'current_date': date.today(),
        'book': Book.objects.filter(id=id)[0]
    }})

```

`books.html`
```html
{% extends 'base.html' %}
{% load static %}

{% block title %}Список книг{% endblock %}

{% block content %}
<ul>
    {% for book in data.books %}
       {% include 'qw.html' with elem=book %}
    {% empty %}
        <li>Список пуст</li>
    {% endfor %}
</ul>
{% endblock %}
```

Содержимое `qw.html` здесь не описано. Его необходимо добавить самостоятельно на основе Лабораторной работы 1.

`book.html`
```html
{% extends 'base.html' %}

{% block title %}Книга №{{ data.book.id }}{% endblock %}

{% block content %}
    <div>Название: {{ data.book.name }}</div>
        <div>Описание: {{ data.book.description }}</div>
{% endblock %}
```

`Итог`

![Создание проекта](assets/6.png)

![Создание проекта](assets/7.png)

## Панель администратора Django

Доступ к панели администратора доступен по ссылке [http://127.0.0.1:8000/admin]()

Для администратора требуется установить пароль в командной строке:
1. python manage.py createsuperuser
2. Указать логин, почту и пароль

![Панель администратора](assets/django_admin.png)

Для добавления доступа к редактированию ваших таблиц в интерфейсе администратора, требуется добавить классы вашей модели в `admin.py`

```python
from .models import Book

admin.site.register(Book)
```

## to-do Использование методов модели