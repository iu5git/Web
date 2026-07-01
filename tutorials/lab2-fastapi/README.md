# Методические указания №2 FastAPI (SQLAlchemy, Alembic, PostgreSQL, Pydantic Settings)

Для выполнения лабораторной работы потребуется установленный Python 3.10+, пакетный менеджер pip, редактор кода (рекомендуется Visual Studio Code или PyCharm) и установленный Docker (для запуска PostgreSQL и Adminer). 

В данной лабораторной работе мы продолжим развитие проекта из первой части: откажемся от хранения данных в памяти, настроим реальную реляционную базу данных PostgreSQL, внедрим систему миграций Alembic, добавим сущности для лайков и реализуем мягкое удаление (soft delete).

## План работы
1. Работа с PostgreSQL (Запуск в Docker)
2. Подключение к БД через IDE и проверка
3. Конфигурация и переменные окружения (Pydantic Settings)
4. Подключение к БД (SQLAlchemy + Alembic)
5. Модели и миграции
6. Получение данных из БД
7. Реализация функционала лайков
8. Удаление услуги через курсор
9. Результат работы и итоговая структура проекта
10. FAQ

---

### 1. Работа с PostgreSQL
PostgreSQL — это мощная реляционная СУБД. На этом этапе мы поднимем её и веб-инструмент Adminer в контейнерах, чтобы иметь изолированную и воспроизводимую среду.

Создайте в корне проекта файл `docker-compose.yml`:
```yaml
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
      POSTGRES_DB: hotels_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  adminer:
    image: adminer:latest
    ports:
      - "8081:8080"
    depends_on:
      - postgres

volumes:
  postgres_data:
```
Запуск выполняется командой:
```bash
docker-compose up -d
```
Проверить статус контейнеров можно командой `docker ps`. Убедитесь, что контейнеры `postgres` и `adminer` находятся в состоянии «Up» (или «Running», если будете проверять в приложении).

![docker](./assets/image-5.png)

---

### 2. Подключение к БД через IDE и проверка
Перед написанием кода полезно убедиться, что база данных доступна. Откройте DBeaver, pgAdmin или DataGrip и создайте новое соединение:
- **Host:** `localhost`
- **Port:** `5432`
- **Database:** `hotels_db`
- **Username:** `myuser`
- **Password:** `mypassword`

![pg-admin](./assets/image-1.png)

Попробуйте сохранить подключение. Если всё прошло успешно, то вы должны видеть пустую базу данных, готовую к наполнению.

---

### 3. Конфигурация и переменные окружения
В реальных проектах параметры подключения не хранят в коде. Мы будем использовать файл `.env` и библиотеку `pydantic-settings` для типизированного чтения настроек.

Установите необходимые пакеты:
```bash
pip install pydantic-settings python-dotenv asyncpg
pip freeze > requirements.txt
```

Создайте в корне проекта файл `.env`:
```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=myuser
DB_PASSWORD=mypassword
DB_NAME=hotels_db
```
*Важно: Добавьте `.env` в файл `.gitignore`.*

Создайте файл `core/config.py` для чтения настроек:
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"

settings = Settings()
```

---

### 4. Подключение к БД (SQLAlchemy и Alembic)
SQLAlchemy позволяет работать с БД через объекты Python. Alembic управляет версиями схемы базы данных (миграциями).

Установите зависимости:
```bash
pip install sqlalchemy alembic
pip freeze > requirements.txt
```

Создайте файл `db/base.py` (основа для моделей):
```python
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
```

Создайте файл `db/session.py` (движок и сессии):
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with async_session_maker() as session:
        yield session
```

Инициализируйте Alembic в корне проекта:
```bash
alembic init alembic
```
Откройте `alembic.ini` и измените строку `sqlalchemy.url` на заглушку:
```ini
sqlalchemy.url = driver://user:pass@localhost/dbname
```
Откройте `alembic/env.py`, импортируйте настройки и **все** модели, и укажите `target_metadata`:
```python
import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

from core.config import settings
from db.base import Base
# Импортируйте здесь все ваши модели, чтобы Alembic их увидел!
from models.hotel import Hotel
from models.user import User
from models.like import Like

config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"})
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

---

### 5. Модели и миграции (Hotels, Users, Likes)
Опишем три сущности - услуги (отели), пользователи и сущность многие-ко-многим (лайки). Мы добавим поле `is_deleted` для мягкого удаления в модель отеля.

Создайте `models/hotel.py`:
```python
from sqlalchemy import Column, Integer, String, Float, Boolean
from db.base import Base

class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String(500), nullable=False)
    image_url = Column(String(255), nullable=False)
    video_url = Column(String(255), nullable=False)
    is_deleted = Column(Boolean, default=False) # Поле для мягкого удаления
```

Создайте `models/user.py`:
```python
from sqlalchemy import Column, Integer, String
from db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, unique=True)
```

Создайте `models/like.py`:
```python
from sqlalchemy import Column, Integer, ForeignKey
from db.base import Base

class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
```

Создайте и примените миграцию:
```bash
alembic revision --autogenerate -m "init hotels, users and likes tables"
alembic upgrade head
```

Откройте Adminer (`http://localhost:8081` с любого браузера), подключитесь по следующим данным: система - PostgreSQL, сервер - postgres, пользователь - myuser, пароль - mypassword, БД - hotels_db. Вы должны увидеть все созданные таблицы.

![tables](./assets/image-2.png)

Перейдите в "SQL-команда" и выполните:
```sql
-- Добавляем тестового пользователя (его ID=1 мы будем использовать для лайков)
INSERT INTO users (id, username) VALUES (1, 'test_user');

-- Добавляем отели
INSERT INTO hotels (id, title, price, description, image_url, video_url, is_deleted)
VALUES
  (1, 'Отель Морской бриз', 5000.0, 'Прекрасный отель на берегу моря.', 'http://localhost:9000/media/hotel.jpg', 'http://localhost:9000/media/hotel_vid.mp4', false),
  (2, 'Отель Горная вершина', 3500.0, 'Уютное шале в горах.', 'http://localhost:9000/media/mountains.jpg', 'http://localhost:9000/media/mountains.mp4', false);
```

![sql-query-tool](./assets/image-3.png)

Проверьте через кнопку "Выбрать" у соответствующих таблиц, что данные были добавлены.

![users](./assets/image-4.png)
![hotels](./assets/image-6.png)

---

### 6. Получение данных из БД
Теперь заменим данные из `data/collections.py` на запросы к БД. Для получения списка отелей будем использовать стандартный ORM-подход SQLAlchemy.

Обновите файл `api/handlers.py`:
```python
from sqlalchemy import select, text
from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
from models.hotel import Hotel
from models.like import Like

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def get_catalog(request: Request, search: str = "", db: AsyncSession = Depends(get_db)):
    stmt = select(Hotel).where(Hotel.is_deleted == False)
    
    if search:
        # ilike работает в PostgreSQL для регистронезависимого поиска
        stmt = stmt.where(Hotel.title.ilike(f"%{search}%"))
        
    result = await db.execute(stmt)
    hotels = result.scalars().all() # scalars() извлекает объекты моделей из результата
    
    return templates.TemplateResponse(
        request=request,
        name="index.html", 
        context={"hotels": hotels, "search": search}
    )

@router.get("/hotel/{hotel_id}")
async def get_hotel_detail(request: Request, hotel_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Hotel).where(Hotel.id == hotel_id)
        
    result = await db.execute(stmt)
    hotel = result.scalar_one_or_none() # извлекаем искомую запись
    
    return templates.TemplateResponse(
        request=request,
        name="hotel.html", 
        context={"hotel": hotel}
    )
```

Теперь мы умеем обрабатывать запросы с параметрами для фильтрации поиска. Добавим поисковую строку в шаблон нашего сайта.

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Каталог отелей</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <h1>Каталог отелей</h1>
    
    <!-- Обновленная форма поиска с классами для корректного отображения -->
    <form class="search-form" action="/" method="GET">
        <input type="text" name="search" placeholder="Поиск по названию" value="{{ search }}">
        <button type="submit">Найти</button>
    </form>

    <ul>
        {% for hotel in hotels %}
        <li>
            <a href="/hotel/{{ hotel.id }}">
                <img src="{{ hotel.image_url }}" alt="{{ hotel.title }}" class="hotel-image">            
                <h2>{{ hotel.title }}</h2>
                <p>Цена: {{ hotel.price }} руб.</p>
            </a>
        </li>
        {% endfor %}
    </ul>
</body>
</html>
```

И теперь сайт взаимодествует с БД.

![step-6](./assets/image-7.png)

---

### 7. Реализация функционала лайков
Добавим возможность ставить лайки. Этот функционал также реализуем через ORM, так как это стандартная операция вставки записи.

Обновите `api/handlers.py`:
```python
from sqlalchemy import select, text
from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
from models.hotel import Hotel
from models.like import Like
from models.user import User

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def get_catalog(request: Request, search: str = "", db: AsyncSession = Depends(get_db)):
    stmt = select(Hotel).where(Hotel.is_deleted == False)
    
    if search:
        # ilike работает в PostgreSQL для регистронезависимого поиска
        stmt = stmt.where(Hotel.title.ilike(f"%{search}%"))
        
    result = await db.execute(stmt)
    hotels = result.scalars().all() # scalars() извлекает объекты моделей из результата

    # Получаем ID отелей, которые уже лайкнул наш тестовый пользователь (user_id = 1)
    # Делаем это одним запросом для эффективности
    liked_result = await db.execute(
        select(Like.hotel_id).where(Like.user_id == 1)
    )
    liked_hotel_ids = {row[0] for row in liked_result.all()}
    
    return templates.TemplateResponse(
        request=request,
        name="index.html", 
        context={
            "hotels": hotels, 
            "search": search,
            "liked_hotel_ids": liked_hotel_ids
        }
    )

@router.get("/hotel/{hotel_id}")
async def get_hotel_detail(request: Request, hotel_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Hotel).where(Hotel.id == hotel_id)
        
    result = await db.execute(stmt)
    hotel = result.scalar_one_or_none() # извлекаем искомую запись
    
    return templates.TemplateResponse(
        request=request,
        name="hotel.html", 
        context={"hotel": hotel}
    )

@router.post("/hotel/{hotel_id}/like")
async def like_hotel(
    hotel_id: int, 
    user_id: int = Form(...), 
    db: AsyncSession = Depends(get_db)
):
    # Проверка существующего лайка через ORM
    stmt = select(Like).where(Like.user_id == user_id, Like.hotel_id == hotel_id)
    result = await db.execute(stmt)
    existing_like = result.scalar_one_or_none()
    
    if existing_like:
        # Если лайк уже стоит, то удаляем запись лайка
        await db.delete(existing_like)

    else:
        # Создание лайка через ORM
        new_like = Like(user_id=user_id, hotel_id=hotel_id)
        db.add(new_like)
    
    # Сохраняем изменения в БД
    await db.commit()
    # Перенаправляем обратно на главную страницу для обновления состояния
    return RedirectResponse(url="/", status_code=303)
```

Обновите шаблон `templates/index.html`, добавив форму лайка и отображение лайкнутого состояния для записи:
```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Каталог отелей</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <h1>Каталог отелей</h1>
    
    <!-- Обновленная форма поиска с классами для корректного отображения -->
    <form class="search-form" action="/" method="GET">
        <input type="text" name="search" placeholder="Поиск по названию" value="{{ search }}">
        <button type="submit">Найти</button>
    </form>

    <ul>
        {% for hotel in hotels %}
        <li>
            <a href="/hotel/{{ hotel.id }}">
                <img src="{{ hotel.image_url }}" alt="{{ hotel.title }}" class="hotel-image">            
                <h2>{{ hotel.title }}</h2>
                <p>Цена: {{ hotel.price }} руб.</p>
            </a>
            
            <div style="margin-top: 15px; display: flex; gap: 10px;">
                <!-- Форма лайка (ORM) -->
                <form action="/hotel/{{ hotel.id }}/like" method="POST">
                    <input type="hidden" name="user_id" value="1">
                    
                    {% if hotel.id in liked_hotel_ids %}
                        <!-- Если уже лайкнуто -->
                        <button type="submit" class="like-btn liked">
                            В избранном
                        </button>
                    {% else %}
                        <!-- Если еще не лайкнуто -->
                        <button type="submit" class="like-btn">
                            Нравится
                        </button>
                    {% endif %}
                </form>
            </div>
        </li>
        {% endfor %}
    </ul>
</body>
</html>
```

Теперь у пользователя есть возможность лайкать отели.

![likes](./assets/image-8.png)

---

### 8. Удаление услуги через курсор
Для удаления воспользуемся курсором (сырым SQL-запросом).

Добавьте обработчик в `api/handlers.py`:
```python
@router.post("/hotel/{hotel_id}/delete")
async def delete_hotel(hotel_id: int, db: AsyncSession = Depends(get_db)):
    # Мы не используем ORM delete(), а выполняем сырой SQL-запрос на обновление флага
    update_query = """
        UPDATE hotels 
        SET is_deleted = true 
        WHERE id = :id
    """
    
    # Выполняем запрос через курсор
    await db.execute(text(update_query), {"id": hotel_id})
    await db.commit()
    
    # Перенаправляем пользователя обратно на главную страницу
    return RedirectResponse(url="/", status_code=303)
```

Обновите шаблон `templates/index.html`, добавив форму удаления записи:
```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Каталог отелей</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <h1>Каталог отелей</h1>
    
    <!-- Обновленная форма поиска с классами для корректного отображения -->
    <form class="search-form" action="/" method="GET">
        <input type="text" name="search" placeholder="Поиск по названию" value="{{ search }}">
        <button type="submit">Найти</button>
    </form>

    <ul>
        {% for hotel in hotels %}
        <li>
            <a href="/hotel/{{ hotel.id }}">
                <img src="{{ hotel.image_url }}" alt="{{ hotel.title }}" class="hotel-image">            
                <h2>{{ hotel.title }}</h2>
                <p>Цена: {{ hotel.price }} руб.</p>
            </a>
            
            <div style="margin-top: 15px; display: flex; gap: 10px;">
                <!-- Форма лайка (ORM) -->
                <form action="/hotel/{{ hotel.id }}/like" method="POST">
                    <input type="hidden" name="user_id" value="1">
                    
                    {% if hotel.id in liked_hotel_ids %}
                        <!-- Если уже лайкнуто -->
                        <button type="submit" class="like-btn liked">
                            В избранном
                        </button>
                    {% else %}
                        <!-- Если еще не лайкнуто -->
                        <button type="submit" class="like-btn">
                            Нравится
                        </button>
                    {% endif %}
                </form>
                <!-- Форма мягкого удаления (Курсор/Raw SQL) -->
                <form action="/hotel/{{ hotel.id }}/delete" method="POST">
                    <button type="submit" class="delete-btn">Удалить</button>
                </form>
            </div>
        </li>
        {% endfor %}
    </ul>
</body>
</html>
```

Теперь у пользователя есть возможность удалять отели.

![delete](./assets/image-9.png)

Добавьте необходимые CSS-стили в `static/css/style.css`, чтобы добавленный нами сегодня функционал выглядел гармонично:
```css
/* Стили для поисковой формы */
.search-form {
    display: flex;
    gap: 10px;
    margin-bottom: 30px;
    max-width: 600px;
}

.search-form input[type="text"] {
    flex: 1;
    padding: 10px 15px;
    border: 2px solid #005df9;
    border-radius: 8px;
    font-size: 16px;
    outline: none;
    background-color: #ffffff;
    color: #333;
}

.search-form button {
    padding: 10px 20px;
    background-color: #005df9;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.2s ease;
}

.search-form button:hover {
    background-color: #0046b8;
}

/* Стили для кнопок действий */
.like-btn {
    background-color: transparent;
    color: #ff4444;
    border: 2px solid #ff4444;
    padding: 8px 12px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    font-weight: bold;
    font-weight: 600;
    line-height: 1.2;
    transition: all 0.2s ease;
}

.like-btn:hover {
    background-color: #ff4444;
    color: white;
}

.like-btn.liked {
    background-color: #ff4444;
    color: white;
    border: 2px solid #ff4444;
}

.like-btn.liked:hover {
    background-color: #cc0000;
    border-color: #cc0000;
}

.delete-btn {
    background-color: #555555;
    color: white;
    border: none;
    padding: 8px 12px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 600;
    line-height: 1.2;
    transition: background-color 0.2s ease;
    border: 2px solid #555555; 
}

.delete-btn:hover {
    background-color: #333333;
}
```

---

### 9. Результат работы и итоговая структура проекта
После реализации всех шагов приложение должно позволять искать отели, ставить им лайки, переходить на страницу с видео и удалять их из выдачи.

![Демонстрация работы приложения](./assets/demo.gif)

Структура вашего проекта должна выглядеть следующим образом:

```text
project_root/
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── alembic.ini
├── api/
│   └── handlers.py
├── core/
│   └── config.py
├── db/
│   ├── base.py
│   └── session.py
├── models/
│   ├── hotel.py
│   ├── user.py
│   └── like.py
├── static/
│   ├── css/
│   │   └── style.css
│   └── img/
├── templates/
│   ├── index.html
│   └── hotel.html
├── .env
├── .gitignore
├── main.py
└── requirements.txt
```

---

### 10. FAQ

**1. Почему мы используем `asyncpg` вместо стандартного `psycopg2`?**  
FastAPI построен на асинхронной архитектуре (ASGI). Использование асинхронного драйвера `asyncpg` позволяет базе данных не блокировать поток выполнения при ожидании ответа, что критически важно для высокой производительности.

**2. Зачем нужен Alembic, если есть параметр `synchronize` или создание таблиц при старте?**  
Автоматическая синхронизация (`synchronize=True` или `create_all`) опасна в продакшене: она может случайно удалить данные или некорректно изменить типы колонок. Alembic позволяет контролировать изменения схемы БД шаг за шагом, хранить историю изменений (версионность) и безопасно применять их на разных окружениях.

**3. В чем преимущество "курсора" (Raw SQL) перед стандартным ORM-методом?**  
Использование сырого SQL через `text()` и построчное чтение (`fetchone`) дает полный контроль над запросом. Это полезно для сложных выборок, оптимизации производительности или при работе с унаследованными базами данных. В учебных целях это демонстрирует понимание того, как фреймворк взаимодействует с СУБД "под капотом", поэтому в задании получение по ID и удаление реализованы именно так.

**4. Почему удаление называется "мягким" (Soft Delete)?**  
При мягком удалении запись физически остается в таблице, но меняется её статус (`is_deleted = true`). Это позволяет сохранить целостность внешних ключей (например, если в будущем вы добавите связанные сущности, они не потеряют связь с отелем), вести аудит действий пользователей и при необходимости восстановить удаленные данные.