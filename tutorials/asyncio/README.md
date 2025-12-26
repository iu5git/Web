
# Методические указания по асинхронным сервисам на FastAPI

## Задачи:
1. Создать асинхронный сервис для выполнения долгой задачи  
2. Показать межсервисное взаимодействие между новым сервисом и сервисом из прошлых лабораторных

## Основы асинхронности в Python: Event Loop, Корутины и Задачи

Перед созданием сервиса важно понять ключевые концепции асинхронного программирования в Python, которые лежат в основе работы asyncio и FastAPI.

### Event Loop (Цикл событий)
Event Loop — это ядро любой асинхронной программы на Python. Это бесконечный цикл, который:
- **Отслеживает** и **распределяет** выполнение различных задач
- **Управляет** сетевыми операциями ввода/вывода
- **Запускает** подпроцессы и колбэки

В отличие от многопоточного подхода, где для каждой задачи создается отдельный поток, Event Loop работает в **одном потоке**, но эффективно переключается между задачами в моменты их простоя (ожидания I/O).

### Корутины (Coroutines)
Корутины — это специальные функции, которые могут **приостанавливать** своё выполнение и **возобновлять** его позже. Они обозначаются ключевым словом `async def`:

```python
async def my_coroutine():
    await asyncio.sleep(1)  # Приостановка выполнения
    return "Задача завершена"
```

Корутина не выполняется сразу при вызове — она возвращает **coroutine object**, который нужно запустить через Event Loop.

### Ключевое слово `await`
`await` используется для приостановки выполнения корутины до завершения другой корутины или Future. Когда корутина встречает `await`, она "говорит" Event Loop: "Я буду ждать, можешь выполнять другие задачи":

```python
async def example():
    # Выполнение приостанавливается здесь
    result = await some_async_function()  
    # Возобновляется после завершения some_async_function
    return result
```

### Задачи (Tasks)
Задачи используются для **запуска корутин параллельно**. Когда корутина обёрнута в задачу с помощью `asyncio.create_task()` или `asyncio.gather()`, она автоматически планируется на выполнение в Event Loop:

```python
async def main():
    # Создаем задачи
    task1 = asyncio.create_task(coroutine1())
    task2 = asyncio.create_task(coroutine2())
    
    # Задачи выполняются "параллельно"
    results = await asyncio.gather(task1, task2)
```

## Разница между I/O-bound и CPU-bound операциями

Прежде чем создавать асинхронный сервис, важно понять, для каких задач подходит асинхронность.

### I/O-bound операции (Input/Output - Ввод/Вывод)

Это операции, которые большую часть времени **ждут** ответа от внешних систем:

- **Сетевые запросы** (HTTP, API вызовы)
- **Работа с базами данных**
- **Чтение/запись файлов**
- **Ожидание ответа от внешних сервисов - наш случай**

**Характеристики:**
- Много времени тратится на ожидание
- Процессор простаивает
- Идеальны для асинхронности

**Пример в нашем сервисе:** Ожидание расчета суммы в рублях (имитация обращения к внешнему API)

### CPU-bound операции (Central Processing Unit - Центральный процессор)

Это операции, которые требуют **интенсивных вычислений**:

- **Сложные математические расчеты**
- **Обработка изображений/видео**
- **Машинное обучение**
- **Шифрование данных**

**Характеристики:**
- Процессор постоянно занят вычислениями
- Нет простоев для ожидания
- Не подходят для чистого asyncio (нужны потоки)

**Важно:** Asyncio эффективен для I/O-bound операций, но для CPU-bound нужны другие подходы (потоки, процессы).

## Создание приложения на FastAPI

FastAPI — современный асинхронный веб-фреймворк для Python, построенный на Starlette и использующий asyncio для асинхронной обработки запросов.

### Подготовка окружения

Создайте новую директорию для проекта:

```bash
mkdir lab8-async-fastapi
cd lab8-async-fastapi
```

Создайте виртуальное окружение и установите зависимости:

```bash
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn httpx
```

## Синхронный веб-сервер

Сначала создадим синхронную версию сервиса, чтобы понять проблему блокирующих операций. Этот сервис будет принимать запросы с данными для конвертации валют и последовательно рассчитывать суммы в рублях.

### Создание файла `main_sync.py`

Создайте файл `main_sync.py`:

```python
from fastapi import FastAPI, HTTPException
import time

app = FastAPI()

MAIN_SERVICE_URL = "http://localhost:8080/api/exchange_result"
SECRET_TOKEN = "MY_SECRET_TOKEN"

def calculate_bill_values(bills: list, rate: float) -> list:
    result = []
    for bill in bills:
        time.sleep(2)
        subtotal_rub = bill["denomination"] * bill["count"] * rate
        print(  
    f"Рассчитана купюра {bill['denomination_id']}: {subtotal_rub:.2f} RUB")
        result.append({
            "denomination_id": bill["denomination_id"],
            "subtotal_rub": round(subtotal_rub, 2)
        })
    return result

@app.post("/api/exchange_sync")
def exchange_sync(data: dict):
    if not data.get("request_id") or not data.get("exchange_rate") or not data.get("bills"):
        raise HTTPException(status_code=400, detail="Invalid payload")
    
    breakdown = calculate_bill_values(data["bills"], data["exchange_rate"])
    
    return {"status": "completed"}
```

### Запуск синхронного сервера

```bash
uvicorn main_sync:app --reload --host 0.0.0.0 --port 8000
```

### Тестирование синхронного сервера

Отправьте запрос с данными для конвертации:

```bash
curl -X POST "http://localhost:8000/api/exchange_sync" \
  -H "Content-Type: application/json" \
  -d '{
    "request_id": "sync_test",
    "exchange_rate": 75.5,
    "bills": [
      {
        "denomination_id": 1,
        "denomination": 10.0,
        "count": 5
      },
      {
        "denomination_id": 2,
        "denomination": 20.0,
        "count": 3
      }
    ]
  }'
```

**Вывод в консоли синхронного сервера:**
```
Рассчитана купюра 1: 377.50 RUB  # ← через 2 секунды
Рассчитана купюра 2: 453.00 RUB  # ← еще через 2 секунды
```

**Проблема:** Каждый расчет занимает 2 секунды, для 2 купюр общее время — 4 секунды. Сервер блокируется на всё это время и не может обрабатывать другие запросы.

## Асинхронный веб-сервер

Теперь создадим асинхронную версию сервиса. Для лучшей организации кода разделим его на несколько файлов.

### Структура проекта

```
lab8-async-fastapi/
├── app/
│   ├── __init__.py
│   ├── main.py              # Точка входа FastAPI
│   ├── config.py            # Конфигурация
│   ├── services/
│   │   ├── __init__.py
│   │   └── exchange.py      # Бизнес-логика расчета
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints.py     # Эндпоинты
│   └── core/
│       └── background.py    # Фоновые задачи
├── requirements.txt
└── README.md
```

### 1. Конфигурация: `app/config.py`

```python
import os

class Settings:
    MAIN_SERVICE_URL = os.getenv("MAIN_SERVICE_URL", "http://localhost:3001")
    SECRET_TOKEN = os.getenv("SECRET_TOKEN", "MY_SECRET_TOKEN")
    
    @property
    def exchange_result_url(self) -> str:
        return f"{self.MAIN_SERVICE_URL}/api/exchange_result"

settings = Settings()
```

### 2. Сервис расчета: `app/services/exchange.py`

```python
import asyncio
import random
from typing import List, Dict

async def calculate_single_bill_async(bill: Dict, rate: float) -> Dict:
    await asyncio.sleep(random.uniform(1, 3))
    subtotal_rub = bill["denomination"] * bill["count"] * rate
    print(  
    f"Рассчитана купюра {bill['denomination_id']}: {subtotal_rub:.2f} RUB")
    return {
        "denomination_id": bill["denomination_id"],
        "subtotal_rub": round(subtotal_rub, 2)
    }

async def calculate_bill_values_async(bills: List[Dict], rate: float) -> List[Dict]:
    tasks = [calculate_single_bill_async(bill, rate) for bill in bills]
    return await asyncio.gather(*tasks)
```

### 3. Фоновые задачи: `app/core/background.py`

```python
import httpx
from typing import List, Dict
from app.config import settings
from app.services.exchange import calculate_bill_values_async

async def send_exchange_result_async(request_id: str, exchange_rate: float, bills: List[Dict]):
    breakdown = await calculate_bill_values_async(bills, exchange_rate)
    
    async with httpx.AsyncClient() as client:
            await client.put(
            settings.exchange_result_url,
            json={
                "token": settings.SECRET_TOKEN,
                "request_id": request_id,
                "breakdown": breakdown
            }
        )
```

### 4. Эндпоинты: `app/api/endpoints.py`

```python
from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.core.background import send_exchange_result_async

router = APIRouter(prefix="/api", tags=["exchange"])

@router.post("/exchange_async")
async def submit_request(data: dict, background_tasks: BackgroundTasks):
    if not data.get("request_id") or not data.get("exchange_rate") or not data.get("bills"):
        raise HTTPException(status_code=400, detail="Invalid payload")
    
    background_tasks.add_task(
        send_exchange_result_async,
        request_id=data["request_id"],
        exchange_rate=data["exchange_rate"],
        bills=data["bills"]
    )
    
    return {"status": "ok"}
```

### 5. Основное приложение: `app/main.py`

```python
from fastapi import FastAPI
from app.api.endpoints import router

app = FastAPI(title="Async Exchange Service")

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Async Exchange Service is running"}
```

### 6. Зависимости: `requirements.txt`

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
httpx==0.25.1
```

### Запуск асинхронного сервера

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Тестирование асинхронного сервера

Отправьте запрос с данными для конвертации:

```bash
curl -X POST "http://localhost:8000/api/exchange_async" \
  -H "Content-Type: application/json" \
  -d '{
    "request_id": "async_test",
    "exchange_rate": 75.5,
    "bills": [
      {
        "denomination_id": 1,
        "denomination": 10.0,
        "count": 5
      },
      {
        "denomination_id": 2,
        "denomination": 20.0,
        "count": 3
      }
    ]
  }'
```

**Вывод в консоли асинхронного сервера:**
```
Рассчитана купюра 2: 453.00 RUB  # ← в течение 2 секунд
Рассчитана купюра 1: 377.50 RUB  # ← в течение 2 секунд
```

## Сравнение производительности

**Синхронный сервер:**
- Ответ приходит через 4 секунды (2 купюры × 2 секунды)
- Купюры рассчитываются последовательно: вывод каждой через 2 секунды
- Сервер блокирован на всё время расчета

**Асинхронный сервис:**
- Ответ приходит мгновенно (статус "ok")
- Купюры рассчитываются параллельно: вывод обеих в течение 2 секунд
- Общее время расчета ~2 секунды (время самой долгой купюры)
- Сервер продолжает обрабатывать другие запросы

**Разница в скорости:** При 2 купюрах асинхронный подход работает в 2 раза быстрее!

## Тестирование межсервисного взаимодействия

Для тестирования в качестве примера будет использоваться этот [основной сервис](https://github.com/Mallartt/main-service-nestjs)

Проверим работу асинхронного сервера. Отправляем запрос, и нам спустя несколько миллисекунд приходит ответ со статусом 200. Спустя примерно 5-10 секунд данные на основном сервере из предыдущих лабораторных обновляются.

**Содержимое PUT запроса:**
```json
{
  "token": "MY_SECRET_TOKEN",
  "request_id": "async_test",
  "breakdown": [
    {
      "denomination_id": 1,
      "subtotal_rub": 377.5
    },
    {
      "denomination_id": 2,
      "subtotal_rub": 453.0
    }
  ]
}
```

## Преимущества асинхронности в asyncio

### 1. Высокая производительность при I/O-bound операциях

**Синхронный:**
```python
def calculate_2_bills():
    time.sleep(2)  # Купюра 1
    time.sleep(2)  # Купюра 2
    # Итого: 4 секунды
```

**Асинхронный:**
```python
async def calculate_2_bills():
    await asyncio.sleep(2)  # Обе купюры
    await asyncio.sleep(2)  # рассчитываются
    # Итого: ~2 секунды
```

### 2. Масштабируемость

Один процесс asyncio может обрабатывать тысячи одновременных запросов. И не будет ограничен числом потоков.

### 3. Эффективное использование ресурсов

По сравнению с многопоточным подходом, asyncio использует кооперативную многозадачность, что уменьшает накладные расходы на переключение контекста. 

### 4. Читаемость кода

Синтаксис `async/await` делает асинхронный код похожим на синхронный, что упрощает его понимание и поддержку. В отличии от ThreadPoolExecutor, где есть сложные колбэки и futures, а так же ручное управление потоками

## Заключение

Созданный асинхронный сервис демонстрирует преимущества asyncio для I/O-bound операций. При расчете 2 купюр:

- **Синхронный подход:** 4 секунды, вывод каждой купюры через 2 секунды, сервер блокирован
- **Асинхронный подход:** ~2 секунды, вывод обеих купюр в течение 2 секунд, сервер отзывчив

**Ключевой вывод:** Asyncio эффективен для задач, где много времени тратится на ожидание (I/O-bound), но не для интенсивных вычислений (CPU-bound). Понимание этой разницы помогает выбирать правильный подход для разных типов задач в веб-разработке.
