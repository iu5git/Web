# Настройка ограничений на вызов методов веб-сервиса для разных ролей пользователей

## Разрешения
Подробно можно прочитать вот [здесь.](https://django.fun/ru/docs/django-rest-framework/3.12/api-guide/permissions/)

Разрешения используются для предоставления или запрета доступа различных классов пользователей к различным частям API. Политика разрешений по умолчанию может быть установлена с помощью параметра `DEFAULT_PERMISSION_CLASSES`. Например, мы хотим дать аутентифицированным пользователям возможность выполнять любые запросы, а анонимным - только запросы на чтение. Тогда в файле `settings.py` нашего проекта нужно указать:
```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ]
}
```

Разрешения в REST-фреймворке всегда определяются как список классов разрешений. Можно установить разрешения для конкретного представления, например:
```python
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class ExampleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'status': 'Запрос разрешен'
        }
        return Response(content)
```

В случае функциональных представлений:
```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def example_view(request, format=None):
    content = {
        'status': 'Запрос разрешен'
    }
    return Response(content)
```

## Составление разрешений с помощью побитовых операторов

Перечисленных способов недостаточно для нашего проекта. Аутентифицированные пользователи у нас делятся на клиента, менеджера и администратора. Клиент должен иметь доступ только к части запросов. Например, он может выполнить запрос на запись при добавлении нового бронирования, но не может добавить новую услугу. Поэтому нам необходимо реализовать пользовательские разрешения.

Предположим, наша модель пользователя `User` содержит, помимо прочих, следующие логические поля:
- `is_staff` - показывает, является ли пользователь менеджером;
- `is_superuser` - показывает, является ли пользователь админом.

Создадим файл `permissions.py`:
```python
from rest_framework import permissions


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_staff or request.user.is_superuser))


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)
        
```

Здесь мы переопределили класс `BasePermission` и реализовали метод `has_permission`, который возвращает `True`, если пользователь `request.user` имеет право выполнить запрос `request`, и `False` в противном случае. В классе `IsManager` этот метод проверяет, является ли пользователь менеджером (или администратором, т.к. ему тоже доступны полномочия менеджера). В классе `IsAdmin` метод проверяет, является ли пользователь администратором.

Теперь добавим в файл `views.py` проверку разрешений при попытке выполнить какой-либо метод API. 
Предположим, у нас есть класс `BookViewSet`, имеющий следующие методы:
- `list` - возвращает список книг;
- `post` - добавляет новую книгу;
- `destroy` - удаляет книгу из списка.

Нужно, чтобы метод `list` был доступен всем пользователям, а методы `post` и `destroy` - только менеджеру, который, согласно нашему заданию, имеет право редактировать таблицу услуг.

```python
class BookViewSet (viewsets.ModelViewSet):
    """api endpoint для просмотра и редактирования списка книг"""
    (...)
    def get_permissions(self):
        if self.action in ['list']:
            permission_classes = [IsAuthenticatedOrReadOnly]
        elif self.action in ['post', 'destroy']:
            permission_classes = [IsManager]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        (...)

    def post(self, request, *args, **kwargs):
        (...)

    def destroy(self, request, pk=None, **kwargs):
        (...)
        
```
Таким образом, мы разделили методы на группы на основании того, какое разрешение нужно проверять при попытке вызова этих методов. Если аутентифицированный пользователь попытается выполнить запрос, который ему не разрешено выполнять, он получит ответ ` 403 Permission Denied`.

