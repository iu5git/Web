# Tauri методические инструкции

## План
- [Создание простого Back-End'а](#создание-простого-back-endа)
    * [Шаг 1: Установка необходимых инструментов](#шаг-1-установка-необходимых-инструментов)
    * [Шаг 2: Инициализация проекта](#шаг-2-инициализация-проекта)
    * [Шаг 3: Инициализация проекта и установка Express](#шаг-3-инициализация-проекта-и-установка-express)
    * [Шаг 4: Создание сервера с Express](#шаг-4-создание-сервера-с-express)
    * [Шаг 5: Запуск сервера](#шаг-5-запуск-сервера)
- [Разработка Tauri приложения](#разработка-tauri-приложения)
    * [Шаг 1: Создание нового Tauri приложения](#шаг-1-создание-нового-tauri-приложения)
    * [Шаг 2: Конфигурация Tauri приложения](#шаг-2-конфигурация-tauri-приложения)
    * [Шаг 3: Запуск Tauri приложения](#шаг-3-запуск-tauri-приложения)
    * [Шаг 4: Разработка frontend'а](#шаг-4-разработка-frontendа)
    * [Шаг 5: Работа с Tauri API](#шаг-5-работа-с-tauri-api)
    * [Шаг 6: Сборка Tauri приложения](#шаг-6-сборка-tauri-приложения)
- [Настройка Tauri для существующего react проекта](#настройка-tauri-для-существующего-react-проекта)
    * [Шаг 1: Инициализация Tauri](#шаг-1-инициализация-tauri)
    * [Шаг 2: Конфигурация Tauri dev](#шаг-2-конфигурация-tauri-dev)
    * [Шаг 3: Конфигурация Tauri build](#шаг-3-конфигурация-tauri-build)
    * [Шаг 4: Подключение к веб-сервису.](#шаг-4-подключение-к-веб-сервису)
- [Подключение к виртуальной локальной сети с помощью ZeroTier One](#подключение-к-виртуальной-локальной-сети-с-помощью-zerotier-one)
- [Дополнительно: Добавление Middleware для сервера](#дополнительно-добавление-middleware-для-сервера)
    * [Шаг 1: Логирование запросов](#шаг-1-логирование-запросов)
    * [Шаг 2: Установка логгера](#шаг-2-установка-логгера)
    * [Шаг 3: Добавление валидации задач](#шаг-3-добавление-валидации-задач)
    * [Шаг 4: Добавляем валидацию на POST-запрос](#шаг-4-добавляем-валидацию-на-post-запрос)

## Создание простого Back-End'а

### Шаг 1: Установка необходимых инструментов

Перед тем, как начать разрабатывать, убедитесь, что у вас установлены следующие инструменты:

1. Node.js - платформа для выполнения JavaScript кода вне браузера.
2. npm (Node Package Manager) - менеджер пакетов для Node.js (поставляется вместе с Node.js).
3. Rust - язык программирования общего назначения, который будет ядром нашего приложения.
4. Cargo - это инструмент, который позволяет указывать необходимые зависимости для проектов на языке Rust

[Скачать Node.js и npm](https://nodejs.dev)

[Скачать Rust и Cargo](https://doc.rust-lang.org/cargo/getting-started/installation.html)

### Шаг 2: Инициализация проекта

Создайте новую папку для Backend'а и перейдите в нее через терминал или командную строку.

```bash
mkdir notes-backend
cd notes-backend
```

### Шаг 3: Инициализация проекта и установка Express

Используя npm, инициализируйте проект и установите Express.

```bash
npm init -y
npm install express
```

### Шаг 4: Создание сервера с Express

Создайте файл `index.js` и подключите Express.

```javascript
// index.js
const express = require('express');
const app = express();
const port = 3000; // Вы можете использовать любой другой порт

// Добавьте промежуточное ПО (middleware) для обработки JSON
app.use(express.json());

// Простой массив для хранения заметок
let todos = [];

// Роут для получения всех заметок
app.get('/todos', (req, res) => {
  res.json(todos);
  console.log(todos);
});

// Роут для создания новой заметки
app.post('/todos', (req, res) => {
  const { id, title, content } = req.body;
  const newTodo = { id, title, content };
  todos.push(newTodo);
  res.status(201).json(newTodo);
  console.log(todos);
});

// Роут для обновления существующей заметки
app.put('/todos/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const { title, content } = req.body;
  const todoIndex = todos.findIndex((todo) => todo.id === id);

  if (todoIndex !== -1) {
    todos[todoIndex] = { id, title, content };
    res.json(todos[todoIndex]);
  } else {
    res.status(404).json({ error: 'Заметка не найдена' });
  }
});

// Роут для удаления заметки
app.delete('/todos/:id', (req, res) => {
  const id = parseInt(req.params.id);
  todos = todos.filter((todo) => todo.id !== id);
  res.status(204).end();
});

// Старт сервера
app.listen(port, () => {
  console.log(`Сервер запущен на порту ${port}`);
});
```

### Шаг 5: Запуск сервера

Запустите ваш сервер, выполнив следующую команду:

```bash
node index.js
```

Ваш backend для заметок с использованием Express должен быть доступен по адресу `http://localhost:3000` (или другому порту, если вы выбрали другой).

Теперь, когда вы успешно создали backend, вы можете использовать его в своем Tauri приложении.

## Разработка Tauri приложения

### Шаг 1: Создание нового Tauri приложения

Для создания нового Tauri приложения используйте:

```bash
npm create tauri@latest
```
В процессе создания укажите следующие настройки:

![Untitled](assets/settings.png)

### Шаг 2: Конфигурация Tauri приложения

Нужно настроить Tauri приложение в файле `src-tauri/tauri.conf.json`. Этот файл находится в папке src-Tauri вашего проекта и позволяет управлять различными настройками такими, как иконки, заголовок окна, настройки безопасности и т.д.

Для того чтобы разрешить приложению обращаться к серверу, добавьте конфигурацию в `allowlist` так, чтобы он выглядел следующим образом:

```json
"allowlist": {
  "all": false,
  "shell": {
    "all": false,
    "open": true
  },
  "http": {
    "request": true,
    "scope": [
      "http://localhost:3000/**"
    ]
  }
}
```

Убедитесь, что в массиве scope присутствует адрес вашего Backend'а.

### Шаг 3: Запуск Tauri приложения

Перейдите в папку вашего Tauri приложения и запустите его, используя команды:

```bash
npm install
npm run tauri dev
```

Это запустит ваше Tauri приложение в режиме разработки. При изменении файлов с кодом ваш проект будет автоматически перезапускаться.

![Untitled](assets/startapp.png)

### Шаг 4: Разработка frontend'а

В папке `src` вы найдёте JSX файлы - файлы React компонентов. 
Сейчас в файле `App.jsx` сгенерированный код. Изменим его так, чтобы в нём остался только наш будущий компонент:

```jsx
import React from 'react';
import { TodoListPage } from './pages/TodoListPage';
import './styles.css';

function App() {
    return (
        <div className='App'>
            <TodoListPage />
        </div>
    );
}

export default App;
```

Создадим папку `pages`, в которой будут размещены страницы нашего приложения. Добавим в папку компонент первой страницы `TodoListPage.jsx` - он будет отвечать за вывод списка задач и взаимодействие с ними:

```jsx
import React, { useState } from 'react';

export function TodoListPage() {
    // список всех задач
    const [todos, setTodos] = useState([]);

    // новая задача
    const [newTodo, setNewTodo] = useState({ title: '', content: '' });
    
    return (
        <div>
            <h1>Планирование задач</h1>
            <div className='container'>
                <input
                    className='input-title'
                    type='text'
                    placeholder='Название'
                    value={newTodo.title}
                />
                <textarea
                    className='input-content'
                    placeholder='Содержание'
                    value={newTodo.content}
                />
                <button className='button button-success text-lg'>
                  Добавить
                </button>
            </div>
            <hr />
            <div className='container'>
                {todos.map((todo) => (
                    <div className='todo' key={todo.id}>
                        <h3 className='todo-title'>
                            {todo.title}
                        </h3>
                        <p className='todo-content'>
                            {todo.content}
                        </p>
                        <button className='button button-danger text-md'>
                            Удалить
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
}
```

`TodoListPage` должен возвращать JSX-код, который [компилируется](https://ru.legacy.reactjs.org/docs/introducing-jsx.html) в вызовы `React.createElement()`, после чего полученные React-элементы [рендерятся](https://ru.legacy.reactjs.org/docs/rendering-elements.html) в DOM. Мы добавили рендеринг в `TodoListPage` и сделали её экспортируемой.

Теперь, если у нас запущено приложение в режиме разработки, должна быть следующая картина:

![Untitled](assets/5.1.png)

Можно удалить `src/App.css`. Так как приложение использует стили по-умолчанию для своего шаблона, мы отредактируем `src/styles.css` так, чтобы сначала сбросить старые стили, а затем установить новые для приложения:

<details>
<summary>Новые стили `src/styles.css`</summary>

```css
/* Сброс стилей */
/* Указываем box sizing */
*,
*::before,
*::after {
  box-sizing: border-box;
}

/* Убираем внутренние отступы */
ul[class],
ol[class] {
  padding: 0;
}

/* Убираем внешние отступы */
body,
h1,
h2,
h3,
h4,
p,
ul[class],
ol[class],
li,
figure,
figcaption,
blockquote,
dl,
dd {
  margin: 0;
}

/* Выставляем основные настройки по-умолчанию для body */
body {
  min-height: 100vh;
  scroll-behavior: smooth;
  text-rendering: optimizeSpeed;
  line-height: 1.5;
}

/* Удаляем стандартную стилизацию для всех ul и il, у которых есть атрибут class*/
ul[class],
ol[class] {
  list-style: none;
}

/* Элементы a, у которых нет класса, сбрасываем до дефолтных стилей */
a:not([class]) {
  text-decoration-skip-ink: auto;
}

/* Упрощаем работу с изображениями */
img {
  max-width: 100%;
  display: block;
}

/* Указываем понятную периодичность в потоке данных у article*/
article > * + * {
  margin-top: 1em;
}

/* Наследуем шрифты для ввода и кнопок */
input,
button,
textarea,
select {
  font: inherit;
}

/* Удаляем все анимации и переходы для людей, которые предпочитай их не использовать */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}

/* Общие стили */
body {
  font-family: Arial, sans-serif;
  font-size: 16px;
  line-height: 1.5;
  color: #333;
  background-color: #f7f7f7;
  margin: 0;
  padding: 0;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  text-align: center;
}

/* Стили для формы добавления заметок */
.input-title,
.input-content {
  display: block;
  width: 100%;
  margin-bottom: 10px;
  padding: 5px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.input-content {
  resize: vertical;
  min-height: 100px;
}

/* Стили для списка заметок */
.todo {
  background-color: #f7f7f7;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
  margin-bottom: 10px;
}

.todo-title {
  margin-top: 0;
}

.todo-content {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  border-radius: 5px;
}

/* Текст заметки на отдельной страницу */
.large-content {
  white-space: pre-wrap;
  border: 1px solid #ccc;
  border-radius: 5px;
  height: max-content;
  padding: 5px;
}

/* стили кнопок и текста */
.button {
  display: inline-block;
  margin: 10px 10px 0 0;
  border-radius: 5px;
  border: none;
  padding: 5px;
  cursor: pointer;
  transition: ease-in-out 0.3s;
  text-decoration: none;
}

.button:hover {
  transform: scale(1.1);
  transition: ease-in-out 0.3s;
}

.button-success {
  background-color: #00bfff;
  color: #fff;
}

.button-danger {
  background-color: #f16c54;
  color: #fff;
}

.button-light {
  background-color: #f7f7f7;
  color: #333;
}

.button-info {
  background-color: #c975ed;
  color: #fff;
}

.text-lg {
  font-size: 16px;
}

.text-md {
  font-size: 14px;
}

.text-sm {
  font-size: 12px;
}
```
</details>


Теперь приложение должно выглядеть следующим образом:

![Untitled](assets/5.2.png)

Заметим, что если вы попробуете что-нибудь написать в полях `Название` и `Содержание`, то ничего не выйдет. В том числе в консоли вы увидите следующее сообщение:

![Untitled](assets/5.3.png)

Дело в том, что мы отображаем состояние компонента, но никак его не меняем. Для того чтобы изменить состояние, нужно повесить триггер на событие изменения `OnChange`, в котором будет вызываться функция изменения состояния:

```jsx
<div className='container'>
  <input
      className='input-title'
      type='text'
      placeholder='Название'
      value={newTodo.title}
      onChange={(e) => setNewTodo({ ...newTodo, title: e.target.value })}
  />
  <textarea
      className='input-content'
      placeholder='Содержание'
      value={newTodo.content}
      onChange={(e) => setNewTodo({ ...newTodo, content: e.target.value })}
  />
  {/* Код кнопки */}
</div>
```

Теперь ввод работает:

![Untitled](assets/5.4.png)

Теперь займёмся добавлением логики, которая выполнится после нажатия на кнопки.

```jsx
import React, { useState } from 'react';

const TodoListPage = () => {
    // список всех задач
    const [todos, setTodos] = useState([]);

    // новая задача
    const [newTodo, setNewTodo] = useState({ title: '', content: '' });

    // добавление новой задачи
    const handleAddTodo = () => {
        if (!newTodo.title || !newTodo.content) {
            console.error('Поля не должны быть пустыми');
            return;
        };
        const newTodoWithId = { ...newTodo, id: Date.now() };
        setTodos([...todos, newTodoWithId]);
        setNewTodo({ title: '', content: '' });
    };

    // удаление задачи
    const handleDeleteTodo = (id) => {
        const updatedTodos = todos.filter((todo) => todo.id !== id);
        setTodos(updatedTodos);
    };

    {/*return ( ... )*/}
}
```

Мы добавили две функции, изменяющие состояния при добавлении и при удалении заметки. Повесим их на события нажатия кнопок:
```jsx
<button
    className='button button-success text-lg'
    onClick={handleAddTodo}
>
    Добавить
</button>
```
```jsx
<button
    className='button button-danger text-md'
    onClick={() => handleDeleteTodo(todo.id)}
>
    Удалить
</button>
```

Обратите внимание на то, как передаются аргументы функций. 

![Untitled](assets/5.5.png)

Теперь заметки добавляются и удаляются, настало время связаться с нашим сервером!

На данном этапе структура проекта должна выглядеть следующим образом:

```
src
│   main.jsx
│   styles.css
│
├───app
│       App.jsx
│
└───pages
        TodoListPage.jsx
```

Для начала создадим файл `src/api/index.js` и добавим в него все функции нашего сервера:
```javascript
const URL = 'http://localhost:3000/todos';

async function getTodos() {
    const response = await fetch(URL, {
        method: 'GET',
        timeout: 30
    });

    if (response.ok) {
        return response.data;
    } else {
        throw new Error(response.status);
    }
}

async function postTodos(todo) {
    const response = await fetch(URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: Body.json(todo)
    });

    if (response.ok) {
        return response.data;
    } else {
        throw new Error(response.status);
    }
}

async function putTodos(todo) {
    const response = await fetch(`${URL}/${todo.id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: Body.json(todo)
    });

    if (response.ok) {
        return response;
    } else {
        throw new Error(response.status);
    }
}

async function deleteTodos(id) {
    const response = await fetch(`${URL}/${id}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    });

    if (response.ok) {
        return response;
    } else {
        throw new Error(response.status);
    }
}

export {
    getTodos, deleteTodos, putTodos, postTodos
}
```

Важно отметить, что в данном случае мы используем `fetch` из пакета `@tauri-apps/api/http`. Tauri является мультиязычным фреймворком, и одним из основополагающих принципов является осуществление безопасности пользователя. В `tauri.conf.json` был указан параметр `scope`, в котором мы указали разрешённые адреса для запросов. Поэтому, если мы попытаемся сделать запрос на другой адрес, то получим ошибку:

`Uncaught (in promise) url not allowed on the configured scope.`

Благодаря этому мы можем быть уверены в том, что наше приложение не сможет отправлять запросы на вредоносные сайты.

Теперь перепишем наш компонент `TodoListPage` с использованием API:
```jsx
import React, { useEffect, useState } from 'react';
import { deleteTodos, postTodos, getTodos } from '../api';

export function TodoListPage() {

    const [todos, setTodos] = useState([]);
    const [newTodo, setNewTodo] = useState({ title: '', content: '' });

    const handleAddTodo = () => {
        if (!newTodo.title || !newTodo.content) {
            return;
        };
        const newTodoWithId = { ...newTodo, id: Date.now() };
        setTodos([...todos, newTodoWithId]);
        setNewTodo({ title: '', content: '' });

        postTodos(newTodoWithId);
    }

    const handleDeleteTodo = (id) => {
        const updatedTodos = todos.filter((todo) => todo.id !== id);
        setTodos(updatedTodos);

        deleteTodos(id);
    }

    // получение списка задач при загрузке страницы
    useEffect(() => {
        getTodos().then(data => {
            setTodos(data);
        });
    }, [getTodos]);

    {/*return ( ... )*/}
}
```

Теперь мы можем получать список задач при загрузке страницы, добавлять новые и удалять существующие. Но что произойдёт, если текст задачи будет слишком велик?

![Untitled](assets/5.6.png)

Наши css-стили не позволяют отображать слишком объёмный текст. Добавим возможность просмотра отдельной задачи. Для этого необходимо добавить роутинг. Для этого установим [пакет](https://reactrouter.com/) `react-router-dom`:

```bash
npm install react-router-dom
```

Теперь улучшим файловую структуру нашего проекта. Создадим папку `src/app`,  `App.jsx` переименуем в `index.jsx` (не забудте обновить импорт в `src/main.jsx`) и перенесём в папку `src/app`. Здесь же создадим `Router.jsx` со следующим содержимым:
```jsx
import {createBrowserRouter, createRoutesFromElements, Route} from 'react-router-dom';
import { TodoListPage, TodoPage } from '../pages';

export const router = createBrowserRouter(
    createRoutesFromElements(
        <>
            <Route path="/" index exact element={<TodoListPage />}/>
            <Route path=":id" element={<TodoPage />} />
        </>
    )
)
```

Отредактируем `src/app/index.jsx`, добавив `RouterProvider` в качестве корневого элемента, в дальнейшем мы создадим собственный провайдер:

```jsx
import React from 'react';
import {RouterProvider} from 'react-router-dom';
import { router } from './Router.jsx';
import { ListenerProvider } from './ListenerProvider';

function App() {
    return (
        <RouterProvider router={router}>
        </RouterProvider>
    );
}

export default App;
```

Создадим страницу `src/pages/TodoPage.jsx`, которая будет отображать отдельную задачу по её `id`, переданному в адресной строке:

```jsx
import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import {getTodos} from "../api/index.js";

export function TodoPage() {

    const { id } = useParams();
    const [todo, setTodo] = useState();

    useEffect(() => {
        getTodos().then(todos => {
            const todo = todos.find(todo => todo.id == id);
            setTodo(todo);
        })
    }, [id]);

    return (
        <div className='container'>
            <Link to='/'>
                <button className='button button-light text-lg'>
                    🔙 Вернуться
                </button>

            </Link>
            {todo &&
                <div className='vertical-center'>
                    <div>
                        <h1>{todo?.title}</h1>
                        <p className='large-content'>{todo?.content}</p>
                    </div>
                </div>}
            {!todo &&
                <h1>Задача не найдена</h1>
            }
        </div>
    );
}
```

Свяжем `TodoListPage` с `TodoPage` с помощью ссылок:
```jsx
// импорты
import { Link } from 'react-router-dom';

export function TodoListPage() {
  // хуки и хендлеры

  return (
    // ...
      <div className='container'>
        {todos.map((todo) => (
              <div className='todo' key={todo.id}>
                  <h3 className='todo-title'>
                      {todo.title}
                  </h3>
                  <p className='todo-content'>
                      {todo.content}
                  </p>
                  <button
                    className='button button-danger text-md'
                    onClick={() => handleDeleteTodo(todo.id)}
                  >
                      Удалить 
                  </button>
                  <Link
                    to={todo.id.toString()}
                    className='button button-info text-md'
                  >
                      Подробнее
                  </Link>
              </div>
          ))}
      </div>
    // ...
  );
}
```

Осталось только добавить [public API](https://feature-sliced.design/docs/reference/public-api#requirements-for-the-public-api) для страниц `src/pages/index.js`:
```jsx
export { TodoListPage } from './TodoListPage';
export { TodoPage } from './TodoPage';
```

После проделанной работы `todo-app/src` имеет следующую структуру:

```
src
│   main.jsx
│   styles.css
│
├───api
│       index.js
│
├───app
│       index.jsx
│       Router.jsx
│
└───pages
        index.js
        TodoListPage.jsx
        TodoPage.jsx
```

А приложение получилось двустраничным:

![Untitled](assets/5.7.gif)

### Шаг 5: Работа с Tauri API

Tauri API - это набор методов, который позволяет взаимодействовать с операционной системой. Например, с помощью Tauri API можно получить список файлов в папке, в которой запущено приложение, или провести системный вызов.
До этого мы использовали Tauri API для отправки безопасных запросов на сервер, теперь же мы попробуем использовать системные диалоговые окна для отображения ошибок.

В конфигурацию `tauri.conf.json` добавим часть [диалогого API](https://tauri.app/v1/api/js/dialog) в `allowlist`:
```json
"dialog": {
  "confirm": true,
  "message": true
}
```

Импортируем необходимые функции из API:
```jsx
import { message, confirm } from '@tauri-apps/api/dialog';
```

Отредактируем хендлеры в `src/pages/TodoListPage.jsx`:
```jsx
const handleAddTodo = () => {
    if (!newTodo.title || !newTodo.content) {
        return message(
            'Поля не могут быть пустыми',
            { title: 'Ошибка', type: 'error' }
        );
    };
    const newTodoWithId = { ...newTodo, id: Date.now() };
    setTodos([...todos, newTodoWithId]);
    setNewTodo({ title: '', content: '' });

    postTodos(newTodoWithId);
}

const handleDeleteTodo = (id) => {
    confirm('Вы уверены, что хотите удалить задачу?')
        .then(res => {
            if (!res) return;
            const updatedTodos = todos.filter((todo) => todo.id !== id);
            setTodos(updatedTodos);

            deleteTodos(id);
        });
}
```

Отлично! Теперь приложение будет отображать диалоговые окна при попытке удалить или добавить пустую задачу:

![Untitled](assets/6.1.gif)

Во многих приложениях встречается нативное меню, которое открывается по нажатию на кнопку в верхнем левом углу. Давайте добавим такое [меню](https://tauri.app/v1/guides/features/menu) в наше приложение. Для этого необходимо отредактировать `main.rs` в папке `src-tauri/src`:
```rust
// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use tauri::{CustomMenuItem, Menu, Submenu};

fn main() {
    let new_todo = CustomMenuItem::new("new".to_string(), "Новая задача");
    let close = CustomMenuItem::new("quit".to_string(), "Выйти");
    let submenu = Submenu::new("Файл", Menu::new().add_item(new_todo).add_item(close));
    let menu = Menu::new()
        .add_submenu(submenu);

    tauri::Builder::default()
        .menu(menu)
        .on_menu_event(|event| {
            match event.menu_item_id() {
              "quit" => {
                // завершаем работу приложения
                std::process::exit(0);
              }
              "new" => {
                // вызываем событие "new-todo"
                event.window().emit("new-todo", "").unwrap();
              },
              _ => {}
            }
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

Tauri позволяет вызывать события на стороне Rust, а также слушать их на стороне JS. Вместо добавления слушателя на каждой отдельной странице, давайте создадим провайдер (компонент высшего порядка ([HOC](https://ru.legacy.reactjs.org/docs/higher-order-components.html)), исполняющий чисто функциональную часть) `ListenerProvider`, в котором будут слушатели событий. Создадим файл `src/app/ListenerProvider.jsx`:
```jsx
import { useNavigate } from "react-router-dom";
import { listen } from "@tauri-apps/api/event";

export function Listener({ children }) {
    const navigate = useNavigate();

    listen('new-todo', () => {
        navigate('/?new-todo');
    });

    return (
        <>
            {children}
        </>
    );
}
```

Здесь мы слушаем событие `new-todo` и переходим на главную страницу с параметром `new-todo`. С помощью [аргумента](https://react.dev/reference/react/Children) `children` мы можем передавать в провайдер любые компоненты, которые будут обернуты в `ListenerProvider`, на случай если мы добавим еще провайдеры. Давайте обернем провайдер в роутер в `src/app/index.jsx`:
```jsx
// ...импорты
import { ListenerProvider } from './ListenerProvider';

function App() {
    return (
        <RouterProvider router={router}>
            <ListenerProvider/>
        </RouterProvider>
    );
}

export default App;
```

Остаётся научиться читать параметры, переданные в адресной строке. Для этого воспользуемся [хуком](https://reactrouter.com/en/main/hooks/use-search-params) `useSearchParams` из библиотеки `react-router-dom`. Отредактируем `src/pages/TodoListPage.jsx`:
```jsx
// ...импорты
import React, { useState, useEffect, useRef } from 'react';
import { useSearchParams } from 'react-router-dom';

export function TodoListPage() {
    // хуки и хендлеры

    // обработка параметров в адресной строке
    const [searchParams] = useSearchParams();
    // ссылаемся на инпут
    const newTodoRef = useRef();

    useEffect(() => {
        if (searchParams.has('new-todo')) {
            newTodoRef.current.focus();
        }
    }, [searchParams]);

    return (
        // разметка
            <input
                className='input-title'
                type='text'
                placeholder='Название'
                value={newTodo.title}
                ref={newTodoRef}
                onChange={(e) => setNewTodo({ ...newTodo, title: e.target.value })}
            />
        // разметка
    );
}
```

Теперь мы можем использовать нативное меню нашего приложения:

![Untitled](assets/6.2.gif)

```
src
│   main.jsx
│   styles.css
│   
├───api
│       index.js
│       
├───app
│       index.jsx
│       ListenerProvider.jsx
│       Router.jsx
│
└───pages
        index.js
        TodoListPage.jsx
        TodoPage.jsx
```

Ну что ж, наша задача выполнена! Мы создали приложение, которое может работать с диалоговыми окнами, отправлять запросы на сервер и использовать нативное меню. Поздравляю!

### Шаг 6: Сборка Tauri приложения

Когда вы готовы опубликовать ваше Tauri приложение, вы можете выполнить команду:

```bash
tauri build
```

Это соберет ваше приложение для целевой платформы (например, Windows, macOS, Linux), и вы найдете файлы приложения в папке `src-tauri/target/release/bundle`.

## Настройка Tauri для существующего react проекта
В данном разделе будет рассматриваться настройка Tauri 2.0 для существующего проекта React, который был настроен для работы с Github Pages, хотя это не является обязательным требованием.
### Шаг 1: Инициализация Tauri
Первым шагом необходимо установить все те же инструменты: npm, Node.js, Rust и Cargo. После этого необходимо установить 2 библиотеки: @tauri-apps/api и @tauri-apps/cli:
```bash
npm install --save-dev @tauri-apps/api@latest
npm install --save-dev @tauri-apps/cli@latest
```
Опция --save-dev говорит о том что данная библиотека нам нужна для разработки, но не нужна для работы программы (сервера) в нормальном режиме.

После установки библиотек необходимо перейти в файл package.json и указать новый script:
```json
"scripts": {
    "tauri": "tauri",
  }
```
Убедитесь, что у вас была установлена версия Tauri 2.0. Для этого запустите команду:
```bash
npm run tauri info
```
И найдите версию Tauri среди packages:
```
[-] Packages
    - tauri 🦀: 2.1.0
```
После этого мы можем инициализировать проект tauri:
```bash
npm run tauri init

? What is your app name? › test_app
? What should the window title be? › test_app
? Where are your web assets (HTML/CSS/JS) located, relative to the "<current dir>/src-tauri/tauri.conf.json" file that will be created? › ../build
? What is the url of your dev server? › http://localhost:3000
? What is your frontend dev command? › npm run dev
? What is your frontend build command? · npm run build
```
После выполнения данной команды должна появиться папка src-tauri, в которой мы буде работать далее. Файлы, с которыми мы будем работать:
```
src-tauri
│   tauri.conf.json
│   Cargo.toml
│
├───src
│       lib.rs
│
└───capabilities
        default.json
```
Вопросы, на которые вы отвечали при создании Tauri не влияют критично на ваш проект и все параметры, указанные при инициализации, можно найти в `src-tauri/tauri.conf.json` в данных местах:
```json
{
  "productName": "test_app",
  "build": {
    "frontendDist": "../build",
    "devUrl": "http://localhost:3000",
    "beforeDevCommand": "npm run dev",
    "beforeBuildCommand": "npm run build"
  },
  "app": {
    "windows": [
      {
        "title": "test_app",
      }
    ],
  },
}
```
### Шаг 2: Конфигурация Tauri dev
приложение Tauri, как и React может работать в двух режимах: Tauri dev и Tauri build. 

Tauri dev работает за счет запуска react сервера и подключению к нему с помощью url, который мы указали как devUrl `src-tauri/tauri.conf.json`. Затем вместо того чтобы открывать вкладку в браузере, Tauri отрисовывает вкладку сайта в нашем приложении.

Это позволяет изменять React сервер в реальном времени и видеть результаты в приложении без его перезапуска. Кроме этого, мы так же получим доступ к режиму разработчика, в котором можно смотреть ошибки, трафик сети, консоль и.т.д. Для получения доступа в нему в открытом приложении Tauri нажмите правой кнопкой мыши по экрану -> проверить.

Для того чтобы Tauri так могло работать необходимо настроить файл `App.tsx` в папке `src`:

```tsx
import { invoke } from "@tauri-apps/api/core";

function App() {
  useEffect(()=>{
    invoke('tauri', {cmd:'create'})
      .then(() =>{console.log("Tauri launched")})
      .catch(() =>{console.log("Tauri not launched")})
    return () =>{
      invoke('tauri', {cmd:'close'})
        .then(() =>{console.log("Tauri launched")})
        .catch(() =>{console.log("Tauri not launched")})
    }
  }, [])
```

Данный код при запуске Tauri будет пытаться создать окно Tauri и подключиться к нему. При этом сайт все еще можно открыть во вкладке браузера, причем выведется сообщение "Tauri not launched".

На данном этапе, если запустить Tauri командой 
```bash
npm run tauri dev
```
То мы увидим рабочее приложение, которое при правильной настройке проксирования будет получать ответы с сервера.

### Шаг 3: Конфигурация Tauri build
Для того чтобы Tauri build правильно работал, в самом начале необходимо убедиться что и в React проекте и в Tauri нет ошибок, иначе не получиться создать build.

Tauri build отличается от Tauri dev в нескольких важных местах: При прописывании команды
```bash
npm run tauri build
```
Вместо запуска приложения, у вас в каталоге появится папка `src-tauri/target/build`. Данная папка будет содержать исполняемый exe файл вашего приложения. Альтернативно, в папке `bundle` вы сможете найти два разных мастера установки, которые вы можете раздавать другим людям для установки приложения.

Кроме этого, Tauri build работает без использования React сервера и поэтому некоторый функционал, который работает именно за счет существования сервера, как например прокси, не будет работать "из коробки".

Если на данном этапе попытаться запустить Tauri build, то скорее всего вы увидите просто белый экран. Если это так, то сначала проверьте что при запуске приложения в режиме dev нету никаких ошибок, которые могли бы повлиять на работу приложения.

Кроме этого, если вы настраивали React для работы с Guthub Pages, вам необходимо убрать basename из Router в `App.tsx` и base из `vite.config.ts`. Эти изменения надо сделать потому что приложение Tauri с одной стороны использует webView, что означает что приложение Tauri на самом деле работает как браузер, встроенный в приложение, который отрисовывает все html страницы по их url. С другой стороны Tauri не запускает React сервер и поэтому base, который мы настроили в `vite.config.ts` ничего не делает (в то время как в react сервере эта опция перенаправляет нас с адреса '/' на адрес, указанный в base).

После исправления выданных ошибок, ваше Tauri приложение должно запуститься в режиме build, но при этом вместо получения данных с сервера, Tauri будет подгружать моки.

### Шаг 4: Подключение к веб-сервису.

Для подключения к веб-сервису необходимо решить 2 проблемы: настройка ip адресов запросов и обход cors.

Во первых, как было сказано выше, Tauri build, так как он не запускает http-сервер, не выполняет проксирование запросов. Поэтому, во всех fetch запросах и всех img тэгах необходимо напрямую указать ip адрес веб-сервиса к которому мы обращаемся. Важно уточнить, что Tauri не может взаимодействовать с https, поэтому для демонстрации его работы закомментируйте соответствующие строки в `vite.config.ts` Для того, чтобы определить этот адрес достаточно ввести команду `npm run dev -- --host` и выбрать адрес из Network (если один из адресов не подошёл, попробуйте другой, для начала проверьте на `npm run dev`, а уже потом на самом Tauri). Обратите внимание, что ip-адрес изменяется в зависимости от способа и сети подключения к Интернету. Для удобства рекомендуется создать отдельный файл или поле для быстрого изменения данного параметра.
Пример :

Создадим файл `target_config.ts`:
```tsx
const target_tauri = false

export const api_proxy_addr = "http://192.168.0.104:8000"
export const img_proxy_addr = "http://192.168.0.104:9000"
export const dest_api = (target_tauri) ? api_proxy_addr : "api"
export const dest_img =  (target_tauri) ?  img_proxy_addr : "img-proxy"
export const dest_root = (target_tauri) ? "" : "/image_editing_frontend"
```
Данное приложение в зависимости от того, создаем ли мы build для Tauri или нет, меняет несколько констант, которые затем используются в `src/api.tsx`:
```tsx
import { dest_api } from "../target_config"
export const getFiltersByTitle = async (title = ''): Promise<FilterPropWithQueue> =>{
return  fetch(dest_api + '/filters?' + new URLSearchParams({title:title}), {method: "GET", credentials: 'include'})
}
```
В тэгах <img>:
```tsx
<img src={(dest_img + pageData.image) || image_mock}/>
```
А так же в `src/App.tsx`:
```tsx
import { dest_root } from "../target_config";

<BrowserRouter basename={dest_root}>
```
и `vite.config.tsx`:
```ts
import {api_proxy_addr, img_proxy_addr, dest_root} from "./target_config"
export default defineConfig({
   base:dest_root,
   server: { 
       port:3000,
       proxy: {
         "/api": {
           target: api_proxy_addr,
           changeOrigin: true,
           rewrite: (path) => path.replace(/^\/api/, "/"),
         },
         "/img-proxy": {
           target: img_proxy_addr,
           changeOrigin: true,
           rewrite: (path) => path.replace(/^\/img-proxy/, "/"),
         },
       },
     },
})
```

Теперь, если мы запустим Tauri build, то, при условии что firewall был настроен правильно, увидим подгрузку статических ресурсов из Minio. Однако, карточки с услугами все еще не будут отображаться.

Если мы зайдем в консоль нашей машины, на которой запущен веб-сервис, то мы увидим, что запросы до сервера доходят. В чем дело? Проблема заключается в том, что у Tauri по умолчанию все запросы соблюдают политику CORS и поэтому ответы от сервера отвергаются нашим приложением. Для того чтобы это исправить, установим библиотеки tauri-plugin-http и tauri-plugin-cors-fetch. Для этого откроем файл `Cargo.toml` и пропишем:
```
tauri-plugin-http = "2"
tauri-plugin-cors-fetch = "2.1.1"
```
Затем необходимо либо обновить зависимости cargo либо просто заново создать Tauri build.

После установки приложений изменим несколько файлов:

`tauri.conf.json`
```json
{
  "plugins": {
        "http": {
          "enabled": true
        }
    },
   "app": {
    "withGlobalTauri": true,
   }
}
```

Если у вас будут возникать проблемы с подгрузкой фотографий или в целом с работой бэкенда, попробуйте изменить ваш `tauri.conf.json`, добавив этот параметр внутрь секции `app` (не забудьте изменить на свой адрес):

`tauri.conf.json`
```json
  {
    "security": {
      "csp": "default-src 'self'; img-src 'self' http://172.27.61.159:9000 data: blob:; connect-src 'self' http://172.27.61.159:8080 http://172.27.61.159:9000; script-src 'self'; style-src 'self' 'unsafe-inline';"
    }
  }
```

`capabilities/default.json`. В "allow" укажите ip адрес вашего веб-сервиса:
```json
{
  "permissions": [
    "cors-fetch:default",
    {
      "identifier": "http:default",
      "allow": [{ "url": "http://192.168.0.104" }],
      "deny": []
    },
    "core:default",
    "http:allow-fetch",
    "http:allow-fetch-read-body",
    "http:allow-fetch-send"
  ]
}
```
В `src\lib.rs` Добавьте запуск tauri_plugin_cors_fetch:
```rs
#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .setup(|app| {
            if cfg!(debug_assertions) {
                app.handle().plugin(
                    tauri_plugin_log::Builder::default()
                        .level(log::LevelFilter::Info)
                        .build(),
                )?;
            }
            Ok(())
        }).plugin(tauri_plugin_cors_fetch::init())
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

Все. После добавления данных изменений, при создании Tauri build вы должны увидеть отображение результатов, полученных с веб-сервиса.
Если у вас возникнут проблемы с тем, что Tauri build всё равно не взаимодействует с фронтендом, попробуйте обновить `middleware.go` в бэкенде, добавив обход политики CORS. Не забудьте обновить `handler.go`.

`middleware.go` 
```go
func CORSMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
		c.Writer.Header().Set("Access-Control-Allow-Credentials", "true")
		c.Writer.Header().Set("Access-Control-Allow-Headers", "Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization, Accept, Origin, Cache-Control, X-Requested-With")
		c.Writer.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS, GET, PUT, DELETE, PATCH")
		c.Writer.Header().Set("Access-Control-Expose-Headers", "Content-Length, Authorization")
		c.Next()
	}
}
```
## Подключение к виртуальной локальной сети с помощью ZeroTier One

Согласитесь, достаточно неудобно постоянно изменять ip-адрес при смене сети подключения к Интернету. Мы можем избежать этого, используя ZeroTier One. Эта утилита позволяет создать свою виртуальную локальную сеть, благодаря чему мы сможем зафиксировать ip-адрес.

### Шаг 1: Регистрация в ZeroTier

Для начала перейдите на сайт [ZeroTier](https://www.zerotier.com/download/) и установите его на своё устройство. Я рекомендую поставить версию 1.6.6 во избежание проблем со стабильностью работы устройства. Далее необходимо зарегистрироваться в [ZeroTier Central](https://my.zerotier.com/).

### Шаг 2: Создание и настройка своей локальной виртуальной сети

После регистрации перед вами откроется интерфейс приложения. Для создания сети нажмите на кнопку "Create A Network", в таблице появится только что созданная сеть. Нажмите на неё и перейдите в интерфейс настройки. Перед вами появятся вкладки Members, Settings, Flow Rules, Administrators. 

![Untitled](assets/5.7.png)

Здесь вы увидите Network ID - это адрес нашей виртуальной сети. Он используется для установления соединения с нашей сетью. Теперь запустите приложение на своём устройстве. Не пугайтесь, если не откроется окно, ZeroTier UI появился в трее. Скопируйте ID вашей сети из ZeroTier Central и вставьте его в поле Join в ZeroTier UI. Обновите страницу в ZeroTier Central, во вкладке Members должно появится ваше подключенное устройство. В колонке Auth будет красный крест, это означает, что соединение установлено, но заблокировано. Для разблокировки надо выбрать эту сеть и нажать кнопку Authorize. После этого в колонке Auth появится зелёная галочка, что говорит об успешном подключении.

![Untitled](assets/5.8.png)

Если вы используете WSL, то необходимо установить соединение через ZeroTier UI на вашей машине, а также внутри WSL следующим способом, иначе вы не сможете получить доступ к сайту через браузер:
```bash
sudo zerotier-cli join a0cbf4b62a8b8a8e
```

Проверить подключение можно с помощью команды `ping`. IP-адрес выдаётся каждому устройству автоматически, во вкладке Settings можно указать диапазон выдачи, рекомендую поставить `192.168.195.*`. Во вкладке Members рядом с каждым устройством появятся выданные ему IP-адреса.

### Шаг 3: Исправление методов

Отлично, мы создали нашу локальную сеть, осталось изменить все методы получения запросов.
Для начала обновим `vite.conf.ts`, изменив в target адрес на полученный:
```tsx
{
  proxy: {
    "/api": {
      target: "http://192.168.195.38:8080",
      changeOrigin: true,
      secure: false,
    },
    "/test": {
      target: "http://192.168.195.38:9000",
      changeOrigin: true,
      secure: false,
    }
  }
}
```

Если вы всё сделали правильно, то на данном этапе при переходе по адресу `http://192.168.195.38:3000/*` вы должны получить какой-либо ответ от вашего бэкенда (например, получить список всех услуг). Обратите внимание, что GET всех услуг, как и другие методы, теперь вызываются через порт фронтэнда. 
Также при вызове команды `npm run dev` ваш сайт должен корректно отображаться (не забудьте изменить адрес в методах получения картинок), а также в Network в `npm run dev -- --host` добавится ваш новый адрес.

Теперь обновим `tauri.conf.json`, заменив все адреса на полученный нами от ZeroTier:
```json
{
  "build": {
      "frontendDist": "../dist",
      "devUrl": "http://192.168.195.38:3000",
      "beforeDevCommand": "npm run dev",
      "beforeBuildCommand": "npm run build"
    },
  "app":{
    "security": {
      "csp": "default-src 'self'; img-src 'self' http://192.168.195.38:9000 data: blob:; connect-src 'self' http://192.168.195.38:8080 http://192.168.195.38:9000; script-src 'self'; style-src 'self' 'unsafe-inline';"
    }
  }
}
```
Теперь попробуем собрать наше приложение через dev режим, используя `npm run tauri dev`.
Видим успешное взаимодействие с бэкендом: все карточки отрисовываются, фотографии загружаются.

![Untitled](assets/5.9.png)

Осталось проверить build режим, собираем наше приложение через `npm run tauri build`. При запуске собранного приложения видим, что наш фронтэнд не взаимодействует с бэкендом. Это связано с тем, что я писал ранее: наши запросы на бэкенд проходят по порту 3000, т.е. по порту фронтэнда. Запустим отдельно наш фронтэнд через `npm run dev`. Ура, теперь в нашем собранном Tauri build приложении появляются карточки и отображаются фотографии!

## Дополнительно: Добавление Middleware для сервера

Middleware - связующее ПО, которое помогает обмену запросов между приложением и сервером. Оно снижает зависимость от API, позволяет не торопиться с обновлением старого Backend'а и снижает нагрузку.

### Шаг 1: Логирование запросов

Для логирования запросов мы будем использовать библиотеку [morgan](https://github.com/expressjs/morgan). Чтобы ее установить, перейдите в директорию `server` и напишите в командной строке:

```bash
npm install morgan
```

### Шаг 2: Установка логгера

Логгер необходим для фиксации событий в работе веб-ресурса, которая помогает выявлять и исправлять в будущем баги системы или ее сбои.

В файле `index.js` импортируйте `morgan`:

```javascript
const express = require('express');
const app = expres();
const cors = require('cors');
// Импортируем библиотеку
const morgan = require('morgan');
// ... Остальной код
```

Далее добавляем логгер и устанавливаем в режим `'combined'` для более подробного получения данных:

```javascript
// ... Остальной код

app.use(cors());
app.use(express.json());
// Устанавливаем morgan в режим 'combined'
app.use(morgan('combined'));

// ... Остальной код
```

Теперь вы можете проверить работоспособность с помощью тестового запроса:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"title":"Buy groceries"}' http://localhost:3000/todos
```

```bash
curl -X POST -H "Content-Type: application/json" -d '{"content":"Oppenheimer or Barbie???"}' http://localhost:3000/todos
```

### Шаг 3: Добавление валидации задач

После того как мы с помощью `curl` попробовали внести новые данные, можно обратить внимание, что они никак не обрабатываются, т.е. спокойно можно внести запись без заголовка, описания или абсолютно пустую запись.

Чтобы этого избежать, необходимо добавить еще один "слой" Middleware, перейдите в директорию `server` и пропишите в терминале:

```bash
mkdir middleware
```

После этого создайте в этой директории файл `validation.js`.

```javascript
const validateTodo = (req, res, next) => {
    const body = req.body;

    // Проверка наличия поля "id" и "title"
    let error = {};
    if (!body.id) {
        error.id = "ID is required"
    }
    if (!body.title) {
        error.title = "Title is required"
    }
    if (error.id || error.title) {
        return res.status(400).json({ error })
    }

    // Задаем значения по умолчанию для "content" и "completed"
    const content = body.content || '';
    const completed = body.completed || false;

    // Создаем объект с валидированными данными
    req.validatedTodo = {
        id: body.id,
        title: body.title,
        content: content,
        completed: completed
    };

    // Переходим к следующему обработчику
    next();
};

// Экспорт функции валидации
module.exports = {
    validateTodo
};
```

Здесь мы проверяем наличие поле title, если оно будет не заполнено, вернется ошибка с описанием `Title is required`.

Далее, если поля content и completed не заполнены, то мы заполняем их по умолчанию пустой строкой и `false` соответственно.

Функция `next()`, которую мы передаем вместе с параметрами, необходима для того, чтобы с видоизмененным запросом перейти к следующему обработчику.

### Шаг 4: Добавляем валидацию на POST-запрос

Перейдем в файл `/server/todos/app.js` и перепишем POST-запрос.

```javascript
const express = require('express');
const router = express.Router();

const todosController = require('./controller');
const validateTodo = require('../middleware/validation');

/*
*   GET-запрос.
*/

router.post('/', validateTodo, (req, res) => {
    const todo = todosController.postTodo(req.validatedTodo);
    res.send(todo);
});
```

1. Мы поменяли входные параметры, теперь обработчик принимает еще один параметр, нашу функцию `validateTodo`, которая валидирует (проверяет на корректность) запрос.

2. Теперь в метод контроллера мы отправляем свойство `req.validateTodo`, которое пришло к нам из `validateTodo`.

Если попробуем добавить какие-то некорректные данные, например:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"content":"Buy fruits"}' http://localhost:3000/todos
```

Получаем на выходе ошибку:
```json
{
  "error": {
    "title": "Title is required"
  }
}
```

Теперь у вас есть простой CRUD-backend с использованием Express и Tauri приложение, которое может взаимодействовать с этим Backend'ом. Вы можете использовать Tauri для создания кросс-платформенных desktop-приложений, а в будущем и мобильных приложений, обещают авторы Tauri
