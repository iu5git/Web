# Методические указания по выполнению лабораторной работы №7

## Что необходимо сделать в ЛР

# Задачи:

- реализовать сущность пользователя;
- предоставить возможность пользователем создавать и использовать учетные записи;
- связать пользователей с уже имеющимися бизнес-сущностями(фактами).
- подключить авторизацию через VK, SMS и тд.

## Сущность пользователя

Мы уже знаем как создавать и внедрять новые сущности в наше приложение. Например, мы делали это в [третьей лабораторной](../lab3/lab3_tutorial.md)
в пункте написания моделей.

Концептуально сущность пользователя должна содержать его личные данные, такие данные:

- номер телефона
- почта
- имя
- никнейм
- и тд...

Нашу новую модель мы должны связать с уже существующими сущностями.

```python
from django.contrib.auth import models as user_models
from django.contrib.auth.models import PermissionsMixin

class User(user_models.AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    ...
```

## Авторизация и регистрация

Представим ситуацию, мы создаем профиль в какой-либо социальной сети, авторизуемся. Теперь, когда бы мы не перешли во вкладку
с этой социальной сетью, мы всегда (точнее в течении какого-то длительного времени) будем авторизованы. Это достигается при помощи
механизма браузера, называемого cookie.

Куки – это небольшие строки данных, которые хранятся непосредственно в браузере. Они являются частью HTTP-протокола.
Куки обычно устанавливаются веб-сервером при помощи заголовка Set-Cookie. Затем браузер будет автоматически добавлять 
их в (почти) каждый запрос на тот же домен при помощи заголовка Cookie.

Один из наиболее частых случаев использования куки – это аутентификация:

При авторизации на сайте сервер отсылает в ответ HTTP-заголовок Set-Cookie для того, чтобы сохранить куки в браузере 
со специальным уникальным идентификатором сессии («session identifier»). Это идентификатор будет являться ключом уникальным сессии пользователя.

Во время любого следующего запроса к этому же серверу за какими-либо данными браузер посылает на сервер HTTP-заголовок Cookie, 
в которым в формате `<ключ>=<значение>`.
Таким образом, сервер понимает, кто сделал запрос.

Подробнее можно почитать вот здесь: [статья](https://developer.mozilla.org/ru/docs/Web/HTTP/Cookies)

Теперь на данном этапе необходимо на клиентской части создать формы авторизации и регистрации. 
Теперь нам необходимо создать два обработчика на серверной части:

- `POST /authorize` - обработчик для авторизации, принимает логин/телефон/почту и пароль;
- `POST /account/create` - обработчик для регистрации, принимает в себя все заполненные личные данные и создает пользователя.

Опишем организацию аутентификации в Django REST Framework. Благо, в DRF есть встроенный механизм аутентификации пользователей.

Рядом с `INSTALLED_APPS` положим данный конфиг:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}
```

Здесь мы подключаем библиотеки встроенной в DRF аутентификации. 
Далее создадим view для авторизации пользователей.

```python
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

def auth_view(request):
    username = request.POST["username"] # допустим передали username и password
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse("{'status': 'ok'}")
    else:
        return HttpResponse("{'status': 'error', 'error': 'login failed'}")
```

Далее для того, чтобы ограничить неавторизованным пользователем доступ к контенту, создадим view и добавим туда `authentication_classes` и `permission_classes`, например:

```python
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class ExampleView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)
```
