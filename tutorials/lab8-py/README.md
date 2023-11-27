# Методические указания по выполнению лабораторной работы №8

## Задачи:
- Создать асинхронный сервис для отложенного действия

## Асинхронный веб-сервер на Django

Создадим приложение с испольхованием  DRF-фреймворка, как это делалось в 3 и 5 лабораторных. 

Установим пакет requests:

`pip install requests`

В views.py добавим обработчик POST-метода `set_status`, который: 
- принимает запрос с полем "pk", 
- запускает "долгую" функцию get_random_status(pk) в ThreadPoolExecutor, который используется для асинхронного выполнения задач,
- добавляем status_callback, который будет выполняться после завершения задачи,
- добавляем id в обычный словарь queue, чтобы не выполнять дважды запросы насчет одного и того же объекта.

`get_random_status(pk)` после 5-секундной задержки определяет случайное булевое значение и возвращает его и pk.

`status_callback` получает результаты выполнения "долгой" задачи и отправляет put-запрос с новым значением is_growing к исходному серверу (из 3 и 5 лабораторных). 

Выполнение всех задач в executor можно остновить с помощью:
- SIGTERM (`kill -SIGTERM <PID>`)
- SIGINT (`Ctrl-C`)

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import time
import random

import requests

from concurrent import futures
import signal

CALLBACK_URL = "http://0.0.0.0:8000/stocks/"

executor = futures.ThreadPoolExecutor(max_workers=1)
queue = { }

def stop_signal(x, y):
  executor.shutdown(wait=False, cancel_futures=True)

signal.signal(signal.SIGTERM, stop_signal)
signal.signal(signal.SIGINT, stop_signal)

def get_random_status(pk):
    time.sleep(5)
    return {
      "id": pk,
      "status": bool(random.getrandbits(1)),
    }

def status_callback(task):
    try:
      result = task.result()
      print(result)
    except futures._base.CancelledError:
      return
    
    if result["id"] in queue:
        try:
            nurl = str(CALLBACK_URL+str(result["id"])+'/put/')
            answer = {"is_growing": result["status"]}
            requests.put(nurl, data=answer, timeout=3)
        except Exception:
           pass
        del queue[result["id"]]

@api_view(['POST'])
def set_status(request):
    if "pk" in request.data.keys():   
        id = request.data["pk"]

        if id in queue:
            return Response(status=status.HTTP_200_OK)

        task = executor.submit(get_random_status, id)
        task.add_done_callback(status_callback)
        queue.update({ id: task })

        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)
```

urls.py будет выглядеть так:

```python
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', views.set_status, name='set-status'),
]
```
Напомню, что на втором сервере из лабораторных 3-5 вызываемый нами сейчас метод выглядит так и доступен без авторизации:

```python
@csrf_exempt
@api_view(['Put'])
@permission_classes([AllowAny])
@authentication_classes([])
def put_detail(request, pk, format=None):
    """
    Обновляет информацию об акции (для пользователя)
    """
    print(request.data)
    stock = get_object_or_404(Stock, pk=pk)
    serializer = StockSerializer(stock, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

## Тестирование

Проверим работу асинхронного сервера. Отправляем последовательно пару запросов, и нам спустя несколько миллисекунд приходят ответы со статусом 200. 
Спустя примерно 5 секунд данные на сервере из лабораторной 3-5 обновляются. 

![1.png](assets/1.png)
![2.png](assets/2.png)
