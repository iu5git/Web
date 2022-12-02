# Методические указания по выполнению лабораторной работы №7

### Команда курса благодарит Толпарова Натана Руслановича за активное участие в подготовке данного руководства.

## Задачи:

- реализовать сущность пользователя;
- предоставить возможность пользователем создавать и использовать учетные записи;
- связать пользователей с уже имеющимися бизнес-сущностями(фактами).
- подключить авторизацию через VK, SMS и тд.

## Сущность пользователя

Мы уже знаем как создавать и внедрять новые сущности в наше приложение. Например, мы делали это в [третьей лабораторной](../lab3-py/lab3_tutorial.md)
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

## СУБД для хранения сессий

Выше мы использовали встроенные механизмы аутентификации в Django. Но для достаточно нагруженных приложений, это не всегда может быть выгодно по производительности,
так как под капотом у Django для хранения сессий используется подключенная нами ранее MySQL.

Хранить сессий выгодно в in-memory хранилищах, таких как:

- Redis
- Memcache
- Tarantool

Давайте возьмем одну из них и попробуем воссоздать руками хранение и проверку сессий. Для этого будем использовать Redis.


### Установка Redis

Redis официально не поддерживается на Windows. Однако, есть возможность установить Redis на Windows через WSL2.

WSL2 позволяет запускать бинарные файлы Linux нативно на Windows. Чтобы это работало необходима Windows 10 версия 2004 и выше или Windows 11.
Инструкция по включению WSL2 доступна по [ссылке](https://learn.microsoft.com/en-us/windows/wsl/install). Рекомендуется ставить Ubuntu.

Далее выполним действия:

```shell
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list

sudo apt-get update
sudo apt-get install redis
```

Чтобы запустить демон Redis, пишем:
```shell
sudo service redis-server start
```

В итоге получаем:
```shell
redis-cli 
127.0.0.1:6379> ping
PONG
```

6379 - это порт на котором автоматически запускается Redis.

### Использование Redis с Python

Чтобы установить библиотеку для работы с Redis пропишем:

```shell
pip3 install redis
```

Далее рассмотрим пример кода, в котором она используется:

```python
import redis

# создаем инстанс и указываем координаты БД на локальной машине
r = redis.Redis(
    host= 'localhost',
    port= '6379')

r.set('somekey', '1000-7') # сохраняем ключ 'somekey' с значением '1000-7!'
value = r.get('somekey') # получаем значение по ключу
print(value)
```

### Интеграция Redis с Django

Для начала нам нужно канонично встроить подключение к БД через Django. Для этого зайдем в файл `settings.py` и пропишем туда координаты запущенной БД:

```python
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
```

Далее создадим библиотечный инстанс нашего хранилища сессий в файле `views.py`:

```python
from django.conf import settings
import redis

# Connect to our Redis instance
session_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
```

Теперь внутри наших обработчиков мы можем использовать `session_storage` для того, чтобы понять, можно ли данному юзер просматривать контент.
Для этого при авторизации пользователя, мы должно сгенерировать случайное значение (можно использовать uuid_v4), и сохранить запись, 
где ключом будет случайно сгенерированная строка, а значением будет первичный ключ сущности пользователя (в нашем примере это username, т.к. он уникальный). 

Итоговый обработчик `auth_view` преватится во что-то такое:

```python
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
import uuid

def auth_view(request):
    username = request.POST["username"] # допустим передали username и password
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        random_key = uuid.uuid4()
        session_storage.set(random_key, username)
        
        response = HttpResponse("{'status': 'ok'}")
        response.set_cookie("session_id", random_key) # пусть ключем для куки будет session_id
        return response
    else:
        return HttpResponse("{'status': 'error', 'error': 'login failed'}")
```

## Ограничение прав на приложение для гостей

Соответственно в методах, в которых нужно проверить, имеет ли пользователя доступ к запрашиваемой информации, мы должны:

- взять из запроса куки (через `ssid = request.COOKIES["session_id"]`)
- посмотреть есть ли в хранилище сессий такая запись, и достать идентификатор пользователя (`session_storage.get(ssid)`)
- проверить, можно ли данному пользователю смотреть запрошенную информацию (зависит от бизнес-логики вашего проекта)

Предлагаем вам такую проверку написать в коде самостоятельно.

Для продвинутых студентов предлагается логику проверки доступности контента вынести в middleware.
