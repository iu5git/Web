# Методические указания по выполнению лабораторной работы №4

**Цель лабораторной работы** - разработка базового приложения на React, знакомство с жизненным циклом приложения и хуками.

<!-- TODO: ссылка на установку VM -->
<!-- TODO: ссылка на настройку IDE -->

**Если у вас возникают сложности с выполнением данной лабораторной работы или недостаточно знаний по JavaScript рекомендуем посмотреть [курс][iu5-javascript].**

## План

## Введение

### Как жить с API

В предыдущей лабораторной работе мы создали наш сервер на Django REST Framework и написали API.
Теперь попробуем написать сайт, который будет работать с нашим API.
До этого мы использовали Django шаблоны, чтобы показать пользователю интерфейс и отобразить данные, но сейчас так сделать не получится. Когда мы использовали Django шаблоны, то у нас сервер выступал в роли бекенда и фронтенда сразу, то есть в нем была реализовано бизнес логика по работе с данными (бекенд) и шаблонизатор для отдачи html (фронтенд). Сейчас же нас сервер выступает в роли бекенда, который нам просто отдает данные, нам нужно написать приложение, которое будет уметь получать эти данные и выводить пользователю. У нас будет 2 независимых приложения. Бекенд на Django REST и фронтенд на JS. Сегодня в примере будет работать с API по акциям, но немного модифицированном. Приступим к делу.

### Что такое TypeScript

### Что такое JSX/TSX

JSX — расширение синтаксиса JavaScript. Этот синтаксис выглядит как язык шаблонов, но наделён всеми языковыми возможностями JavaScript. В результате компиляции JSX возникают простые объекты — «React-элементы». TSX - это JSX только на языке TypeScript.

React DOM использует стиль именования camelCase для свойств вместо обычных имён HTML-атрибутов. Например, в JSX атрибут `tabindex` станет `tabIndex`. В то время как атрибут `class` записывается как `className`, поскольку слово `class` уже зарезервировано в JavaScript.

## React

React-разработка заключается в описании того, что нужно вывести на страницу (а не в составлении инструкций для браузера, посвящённых тому, как это делать). Это, кроме прочего, означает значительное сокращение объёмов шаблонного кода.

### Component

React-компоненты — это повторно используемые части кода, которые возвращают React-элементы для отображения на странице. Самый простой React-компонент — это простая функция JavaScript, которая возвращает элементы React.

```tsx
import { FC } from 'react'

const Welcome: FC = (props) => {
  return <h1>Привет, {props.name}</h1>;
}
```

Компоненты могут быть классами ES6.

```tsx
import React from 'react'

class Welcome extends React.Component {
  render() {
    return <h1>Привет, {this.props.name}</h1>;
  }
}
```

На данный момент в разработке предпочитают использовать функциональные компоненты. Подробнее о том, как они работают и чем отличаются от классовых можно узнать в [этой статье][habr-react-diff-class-function-component].

Компоненты могут состоять из других компонентов, так что по сути целая страница может считаться компонентом.

### Element

React-элементы — это составляющие блоки React-приложений. Их можно перепутать с более известной концепцией «компонентов», но в отличие от компонента, элемент описывает то, что вы хотите увидеть на экране. React-элементы иммутабельны.

В стандартном React-приложении состояние является объектом. Процесс согласования (reconciliation process) в React определяет, необходимо ли производить повторный рендеринг объекта, поэтому ему нужно следить за изменениями этого объекта.

Другими словами, если React не сможет определить изменение объекта, он не обновит виртуальный DOM.

Иммутабельность позволяет наблюдать за такими изменениями. Это, в свою очередь, позволяет React сравнивать старое и новое состояния объекта и на основе этого сравнения перерисовывать объект.

### Props

`props` (пропсы) — это входные данные React-компонентов, передаваемые от родительского компонента дочернему компоненту.

Пропсы предназначены для чтения. Если требуется изменять данные, то необходимо использовать state (состояние приложения).

В любом компоненте доступны `props.children`. Это контент между открывающим и закрывающим тегом компонента. Например:

```tsx
<React.StrictMode>
  <App />
</React.StrictMode>
```

Для `React.StrictMode` в **children** попадает компонент `App`.

### State

Компонент нуждается в `state`, когда данные в нём со временем изменяются. Например, компоненту `Checkbox` может понадобиться состояние `isChecked`.

Разница между пропсами и состоянием заключается в основном в том, что состояние нужно для управления компонентом, а пропсы для получения информации.

Если возникла необходимость изменять пропсы, то нужно вынести их в состояние родительского компонента и пробрасывать в текущий компонент не только этот объект, но и функцию, которая изменит его.

Прежде чем перейти к примеру работы с состоянием, ознакомимся с жизненным циклом приложения.

## Создание проекта

Для разработки мы будем использовать шаблон [Vite React TS][vite-template-project] - это удобная среда для создания первого простого приложения на **React**.

Для создания первого проекта выполняем следующее.

```shell
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install
```

После выполнения этих команд у нас будет готовое приложение. "Под капотом" нашего приложения используется язык [Typescript][typescript], библиотека [React][react] и сборщик [Vite][vite].

Для удобства разработки внесем изменения в `vite.config.ts`, чтобы у нас всегда локальный сервер запускался на 3000 порту.

```ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  server: { port: 3000 },
  plugins: [react()],
})
```

Для работы с приложением у нас есть 2 основные команды:

* `npm run dev` - запуск локального сервера для разработки
* `npm run build` - создание оптимизированной сборки приложения

Запустим команду `npm run dev`, чтобы запустить локальный сервер для разработки. Страница автоматически перезагрузиться, если вы внесете изменения в код. Вы сможете увидеть ошибки сборки и предупреждения в консоли.

![Фото 1](./assets/1.png)

## Структура проекта

В папке проекта у нас будут следующие файлы:

* `package.json` - основной файл с информацией о проекте
* `package-lock.json` - лок файл со списком зависимостей
* `vite.config.ts` - конфигурационный файл сборщика Vite
* `tsconfig.json` - конфигурационный файл TypeScript
* `tsconfig.node.json` - конфигурационный файл TypeScript при запуске на Node
* `.eslintrc.cjs` - конфигурационный файл Eslint
* `index.html` - основной файл нашего приложения. Он будет первым загружаться, когда пользователь заходит на страницу
* `src/main.tsx` - основной TS файл нашего приложения. Тут мы запускаем отрисовку приложения
* `src/App.tsx` - верстка приложения. Логотип Vite и React

![Фото 2](./assets/2.png)

Рассмотрим поподробнее основные файлы нашего приложения.

### index.html

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Vite + React + TS</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

Файл `index.html` первым загружается при стартпе приложения у пользователя. Рассмотрим основные части:

* `link` - загрузка иконки вкладки в браузере
* `title` - название вкладки в браузере
* `meta` - установка технической информации
* `script` - подключение основного TS файла нашего проекта. Когда он загрузится, то начнет исполнятся и нарисует логотипы Vite и React
* `div id=root` - технический тег. В него React будет вставлять код приложения

### src/main.tsx

```tsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```

Файл `src/main.tsx` загружается с нашего html файла и после исполнения начнет рендерить наше приложение. Рассмотрим основные части:

* `document.getElementById('root')` - получение технического тега из `index.html` файла
* `React.StrictMode` - инструмент для обнаружения потенциальных проблем в приложении

### src/App.tsx

```tsx
import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div>
        <a href="https://vitejs.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App
```

Это основной компонент нашего приложения. В нем происходит отрисовка логотипов Vite и React.

## Роутинг

Вне зависимости от выбранной предметной области нашего приложение может состоять из нескольких страниц. Для удобного перехода между страницами будет использовать роутинг.

Для этого нам необходимо установить библиотеки `react-router-dom`, `@types/react-router-dom`

```shell
npm i react-router-dom
npm i @types/react-router-dom -D
```

Сделаем так, чтобы в `main.tsx` у нас было несколько страниц.

```tsx
import React from 'react'
import ReactDOM from 'react-dom/client'

import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import './index.css'

const router = createBrowserRouter([
  {
    path: '/',
    element: <h1>Это наша стартовая страница</h1>
  },
  {
    path: '/new',
    element: <h1>Это наша страница с чем-то новеньким</h1>
  }
])

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
)
```

**Главная страница**

![Фото 3](./assets/3.png)

**Страница `/new`**

![Фото 4](./assets/4.png)

Роутер позволяет нам перемещаться между разными страницами без перезагрузки. Для этого можно использовать стандартный тег `a`.

```tsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import { createBrowserRouter, RouterProvider, Link } from 'react-router-dom'
import './index.css'

const router = createBrowserRouter([
  {
    path: '/',
    element: <h1>Это наша стартовая страница</h1>
  },
  {
    path: '/new',
    element: <h1>Это наша страница с чем-то новеньким</h1>
  }
])

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ul>
      <li>
        <a href="/">Старт</a>
      </li>
      <li>
        <a href="/new">Хочу на страницу с чем-то новеньким</a>
      </li>
    </ul>
    <hr />
    <RouterProvider router={router} />
  </React.StrictMode>,
)
```

**Главная страница**

![Фото 5](./assets/5.png)

**Страница `/new`**

![Фото 6](./assets/6.png)

Теперь вы знакомы с роутингом в приложении. Если потребуется обрабатывать какую-то информацию из адресной строки или использовать какой-то **особый роутер**, то подробнее о типах и работе роутеров можно ознакомиться в документации React или же на сайте [React Router][react-router] с готовыми примерами.

## Жизненный цикл React приложения

Давайте рассмотрим каждый жизненный этап, включая методы, с ними связанные.

### Монтирование

Классовые компоненты тоже являются классами,  так что в первую очередь будет вызван constructor(). В нем мы выполняем инициализацию состояния компонента.

Далее компонент запускает getDerivedStateFromProps(), потом запускается render(), возвращающий JSX. React «монтируется» в DOM.

Затем происходит запуск метода componentDidMount(), в котором выполняются все асинхронные процессы, описанные разработчиком. После этого компонент можно считать успешно "рожденным"

### Обновление

Данный этап запускается во время каждого изменения состояния либо свойств. Как и в случае с монтированием, происходит вызов метода getDerivedStateFromProps(), однако в этот раз уже без конструктора.

Потом происходит запуск shouldComponentUpdate().

В shouldComponentUpdate() можно сравнить состояния **до** и **после** , чтобы лишний раз не перерисовывать компонент.

Потом React запустит componentDidUpdate(). Как и в случае с componentDidMount(), его можно применять для асинхронных вызовов либо управления DOM.

### Размонтирование

Когда компонент прожил свою жизнь, наступает размонтирование — последний жизненный этап. React выполняет запуск componentWillUnmount() непосредственно перед удалением из DOM. Данный метод применяется при закрытии всех открытых соединений типа web-сокетов либо тайм-аутов.

В этой лабораторной работе мы будем работать с функциональными компонентами.

## Функциональные компоненты

1. Описание компонентов с помощью чистых функций создает меньше кода, а значит его легче поддерживать.
2. Чистые функции намного проще тестировать. Вы просто передаете props на вход и ожидаете какую то разметку.
3. В будущем чистые функции будут выигрывать по скорости работы в сравнении с классами из-за отсутствия методов жизненного цикла

## Хуки

Хуки — нововведение в React 16.8, которое позволяет использовать состояние и другие возможности React без написания классов.

Хук - функция, которая позволяет добавлять пользовательскую логику в события жизненного цикла приложения. **Они не будут работать в классовых компонентах!**

## Хук состояния

Допустим, мы хотим инициализировать в классе состояние `count` значением `0`. Для этого в его конструкторе присваиваем `this.state` объект `{ count: 0 }`:

```tsx
import React from 'react'

class Example extends React.Component {
    constructor(props: Props) {
        super(props);
        this.state = {
            count: 0
        };
    }
}
```

В функциональном компоненте нам недоступен `this`, поэтому мы не можем задать или считать состояние через `this.state`. Вместо этого мы вызываем хук `useState` напрямую изнутри нашего компонента.

```tsx
import { FC, useState } from 'react'

const Example: FC = () => {
    // Объявление новой переменной состояния «count»
    const [count, setCount] = useState(0);

    return <div onClick={()=>setCount(count=>count++)}>{count}</div>
}
```

## Хук эффекта

С помощью хука эффекта `useEffect` вы можете выполнять побочные эффекты из функционального компонента. Он выполняет ту же роль, что и `componentDidMount`, `componentDidUpdate` и `componentWillUnmount` в React-классах, объединив их в единый API. Вы можете найти сравнение `useEffect` и этих методов на странице [использование хука эффекта][react-hooks].

```tsx
useEffect(() => {
  // Этот код выполнится на mount`е компонента
        
  return () => {
    // Этот код выполнится на unmount`е компонента
  }

  // Это список зависимостей хука, он будет вызван каждый раз, когда зависимости будут меняться
}, [])
```

Хуки налагают два дополнительных правила для разработки:

* Не вызывайте хуки внутри циклов, условий или вложенных функций.
Они должны выполняться только **на верхнем уровне**.
* Хуки следует вызывать только из функциональных компонентов React и пользовательских хуков.

Пользовательский хук это такая функция JavaScript, внутри которой используются другие хуки. На этот хук распространяются правила хуков, которые описаны ранее.

В [этой статье][habr-react-hooks] можно посмотреть на классные реализации полезных в разработке пользовательских хуков.

# План

1. Введение и установка проекта
2. Роутинг в react приложении
3. Терминология
    1. JSX
    2. Component
    3. Element
    4. Props
    5. State
4. Жизненный цикл react приложения
    1. Монтирование
    2. Обновление
    3. Размонтирование
5. Функциональные компоненты и хуки
    1. Функциональные компоненты
    2. Хуки
        1. Хук состояния
        2. Хук Эффекта
        3. Пользовательские хуки
6. Практика
    1. Пример работы с хуками эффекта и состояния на простом приложении
    2. Разработка с компонентным подходом.Пример работы с API, библиотеками и пользовательскими хуками
7. Полезные ссылки

# Практика

Создадим директорию со страницами нашего приложения:

Пример функционального компонента, на котором можно наблюдать работу с состоянием и жизненным циклом приложения:

```tsx
import React, {useEffect, useState} from 'react';

const data = [
    'Берик Дондаррион',
    'Леди Мелиссандра',
    'Полливер',
    'Уолдер Фрей',
    'Тайвин Ланнистер',
    'Сир Мерин Трэнт',
    'Король Джоффри',
    'Сир Илин Пейн',
    'Гора',
    'Пес',
    'Серсея Ланнистер',
]

function StartPage() {

    // В функциональных компонентах для работы с состоянием можно использовать хук useState()
    // Он возвращает кортеж из двух элементов:
    // 1 элемент - объект состояния
    // 2 элемент - метод который позволит нам обновить состояние
    const [randomName, setRandomName] = useState();

    // Кстати, это хороший пример деструктуризации массива в JavaScript
    const [names, setNames] = useState(data);

    const [showNames, setShowNames] = useState(false);

    // В данном хендлере мы изменяем состояние на какое-то конкретное
    const handleShowNames = () =>{
        setShowNames(true)
    }

    // В данном хендлере мы изменяем состояние на какое-то конкретное
    const handleHideNames = () =>{
        setShowNames(false)
    }

    // В данном хендлере мы изменяем состояние в зависимости от его прошлого значения
    const handleSwitch = () =>{
        // метод из useState может принимать как определенное значение, так и метод,
        // принимающий прошлое значение и возвращающий новое
        setShowNames(state => !state)
    }

    useEffect(()=>{
        console.log('Этот код выполняется только на первом рендере компонента')
        // В данном примере можно наблюдать Spread syntax (Троеточие перед массивом)
        setNames(names=>[...names, 'Бедный студент'])

        return () => {
            console.log('Этот код выполняется, когда компонент будет размонтирован')
        }
    },[])

    useEffect(()=>{
        console.log('Этот код выполняется каждый раз, когда изменится состояние showNames ')
        setRandomName(names[Math.floor(Math.random()*names.length)])
    },[showNames])

    
    return (
        <div>
            <h3>Случайное имя из списка: {randomName}</h3>
            {/*Кнопка для того, чтобы показать имена*/}
            <button onClick={handleShowNames}>Хочу увидеть список имен</button>
            {/*Кнопка для того, чтобы скрыть имена*/}
            <button onClick={handleHideNames}>Хочу скрыть список имен</button>

            {/*Универсальная кнопка*/}
            <button onClick={handleSwitch}>{showNames ? 'Хочу скрыть список имен' :'Хочу увидеть список имен' }</button>

            {/*React отрисует список только если showNames будет равен true, boolean значения игнорируются при отрисовке*/}
            {showNames && <ul>
            {/*Рекомендую почитать про прекрасные встроенные методы массивов в JavaScript    */}
            {names.map((name, index)=>{
                return (
                    <li key={index}>
                        <span>{name}</span>
                    </li>
                )
            })}
            </ul>
            }
        </div>
    );
}

export default StartPage;
```

![Untitled](assets/Untitled%201.gif)

# Практика, которая похожа на настоящую практику

Предположим, у нас уже есть рабочий API (В примере используется API ITunes).

Мы можем получить список сущностей, отфильтровать их и вывести в понятном виде пользователю.

Создадим страницу для отрисовки треков из ITunes

```tsx
import React, {useEffect, useState} from 'react';
import {Card, Col, Row, Button, Spinner} from "react-bootstrap";
import './ITunesPage.css';

const DEFAULT_SEARCH_VALUE = 'radiohead';

const getMusicByName = async (name = DEFAULT_SEARCH_VALUE) =>{
    const res = await fetch(`https://itunes.apple.com/search?term=${name}`)
        .then((response) => {
            return response.json();
        }).catch(()=>{
            return {resultCount:0, results:[]}
        })
    return res
}

function ITunesPage() {

    const [searchValue, setSearchValue] = useState('radiohead');

    const [loading, setLoading] = useState(false)

    const [music, setMusic] = useState([])

    const handleSearch = async () =>{
        await setLoading(true);
        const { results } = await getMusicByName(searchValue);
        await setMusic(results.filter(item => item.wrapperType === "track"));
        await setLoading(false)
    }

    return (
        <div className={`container ${loading && 'containerLoading'}`}>
            {loading && <div className="loadingBg"><Spinner animation="border"/></div>}
            <div className="inputField">
                <input value={searchValue} onChange={(event => setSearchValue(event.target.value))}/>
                <Button disabled={loading} onClick={handleSearch}>Искать</Button>
            </div>
            {!music.length && <div>
                <h1>К сожалению, пока ничего не найдено :(</h1>
            </div>}

            <Row xs={4} md={4} className="g-4">
                {music.map((item, index)=>{
                return<Col >
                <Card key={index} className="card">
                    <Card.Img className="cardImage" variant="top" src={item.artworkUrl100} height={100} width={100}  />
                    <Card.Body>
                        <div className="textStyle">
                            <Card.Title>{item.artistName}</Card.Title>
                        </div>
                        <div  className="textStyle">
                            <Card.Text>
                                {item.collectionCensoredName}
                            </Card.Text>
                        </div>
                        <Button className="cardButton" href={item.trackViewUrl} target="_blank" variant="primary">Открыть в ITunes</Button>
                    </Card.Body>
                </Card>
                </Col>
            })}
            </Row>
    </div>
    );
}

export default ITunesPage;
```

![Untitled](assets/Untitled%202.gif)

Для того, чтобы в будущем было куда удобнее разрабатывать, стоит разделять страницу на компоненты, и разделять логику в разных файлах.

На данном этапе у нас есть тонна кода в одном файле.

Вынесем в директорию components  карточку и поле ввода .

Работу с сетью вынесем в директорию modules

```tsx
import React, {useState} from 'react';
import { Col, Row, Spinner} from "react-bootstrap";
import MusicCard from "../../components/MusicCard";
import InputField from "../../components/InputField";
import { getMusicByName } from '../../modules'
import './ITunesPage.css';

function ITunesPage() {

    const [searchValue, setSearchValue] = useState('radiohead');

    const [loading, setLoading] = useState(false)

    const [music, setMusic] = useState([])

    const handleSearch = async () => {
        await setLoading(true);
        const { results } = await getMusicByName(searchValue);
        await setMusic(results.filter(item => item.wrapperType === "track"));
        await setLoading(false)
    }

    return (
        <div className={`container ${loading && 'containerLoading'}`}>
            {loading && <div className="loadingBg"><Spinner animation="border"/></div>}
            <InputField value={searchValue} setValue={setSearchValue} loading={loading} onSubmit={handleSearch} buttonTitle="Искать"/>
            {!music.length ? <h1>К сожалению, пока ничего не найдено :(</h1>:
                <Row xs={4} md={4} className="g-4">
                {music.map((item, index)=>{
                    return(
                        <Col key={index}>
                            <MusicCard {...item}/>
                        </Col>
                    )
                })}
            </Row>
            }
    </div>
    );
}

export default ITunesPage;
```

```tsx
import {Button} from "react-bootstrap";
import React from "react";
import './InputField.css';

const InputField = ({ value, setValue, onSubmit, loading, placeholder, buttonTitle = 'Поиск'}) => {
    return <div className="inputField">
        <input value={value} placeholder={placeholder} onChange={(event => setValue(event.target.value))}/>
        <Button disabled={loading} onClick={onSubmit}>{buttonTitle}</Button>
    </div>
}

export default InputField
```

```tsx
import {Button, Card} from "react-bootstrap";
import React from "react";
import './MusicCard.css';

const MusicCard = ({artworkUrl100, artistName, collectionCensoredName, trackViewUrl}) => {

    return <Card className="card">
        <Card.Img className="cardImage" variant="top" src={artworkUrl100} height={100} width={100}  />
        <Card.Body>
            <div className="textStyle">
                <Card.Title>{artistName}</Card.Title>
            </div>
            <div  className="textStyle">
                <Card.Text>
                    {collectionCensoredName}
                </Card.Text>
            </div>
            <Button className="cardButton" href={trackViewUrl} target="_blank" variant="primary">Открыть в ITunes</Button>
        </Card.Body>
    </Card>
}

export default MusicCard;
```

Теперь, когда мы разделили код, можно приступать к совершенствованию функционала.

Внезапно, у нас появилась необходимость добавить поиск по названию для уже загруженного списка.

Добавим на страницу еще один компонент InputField, который будет отвечать за поиск по автору в загруженном списке

```tsx
import React, {useState} from 'react';
import { Col, Row, Spinner} from "react-bootstrap";
import MusicCard from "../../components/MusicCard";
import InputField from "../../components/InputField";
import { getMusicByName } from '../../modules'
import './ITunesPage.css';

function ITunesPage() {

    const [searchValue, setSearchValue] = useState('radiohead');

    const [filter, setFilter] = useState('');

    const [loading, setLoading] = useState(false)

    const [music, setMusic] = useState([])

    const handleSearch = async () => {
        // Сбрасываем фильтр
        await setFilter('');
        // Ставим загрузку
        await setLoading(true);
        const { results } = await getMusicByName(searchValue);
        // Добавляем в состояние только треки
        await setMusic(results.filter(item => item.wrapperType === "track"));
        // Убираем загрузку
        await setLoading(false)
    }

    const handleFilter = ()=> {
        setMusic(music => music.filter(item=>item.artistName && item.artistName.includes(filter)));
    }

    return (
        <div className={`container ${loading && 'containerLoading'}`}>
            {loading && <div className="loadingBg"><Spinner animation="border"/></div>}
            <InputField value={searchValue} setValue={setSearchValue} placeholder="поиск" loading={loading} onSubmit={handleSearch} buttonTitle="Искать"/>
            <InputField value={filter} setValue={setFilter} placeholder="Автор" loading={loading} onSubmit={handleFilter} buttonTitle="Отфильтровать"/>
            {!music.length ? <h1>К сожалению, пока ничего не найдено :(</h1>:
                <Row xs={1} md={4} className="g-4">
                {music.map((item, index)=>{
                    return(
                        <Col key={index}>
                            <MusicCard {...item}/>
                        </Col>
                    )
                })}
            </Row>
            }
    </div>
    );
}

export default ITunesPage;
```

Для осуществления нашей цели нам потребовалось добавить еще одно состояние и функцию для фильтрации. После добавления нового инпута с фильтрацией, можем видеть результат:

![Untitled](assets/Untitled%203.gif)

В данном примере используется библиотека компонентов react-bootstrap.

К сожалению, на странице отсутствует адаптивная верстка. Учитывая факт, что мы уже ознакомились с пользовательскими хуками, предлагаю экспресс решение для добавления адаптивной верстки на эту страницу.

Компонент Row может принимать пропс md, от которого зависит количество колонок.

Если в момент рендера мы будем знать ширину экрана, то мы сможем регулировать количество колонок в компоненте.

Добавим на страницу наш ранее описанный пользовательский хук `useWindowSize()`

```tsx
  const { width } = useWindowSize();
    const isMobile = width && width <= 600;

    return (
        <div className={`container ${loading && 'containerLoading'}`}>
            {loading && <div className="loadingBg"><Spinner animation="border"/></div>}
            <InputField value={searchValue} setValue={setSearchValue} placeholder="поиск" loading={loading} onSubmit={handleSearch} buttonTitle="Искать"/>
            <InputField value={filter} setValue={setFilter} placeholder="Автор" loading={loading} onSubmit={handleFilter} buttonTitle="Отфильтровать"/>
            {!music.length ? <h1>К сожалению, пока ничего не найдено :(</h1>:
                <Row xs={1} md={isMobile ? 1 : 4} className="g-4">
                {music.map((item, index)=>{
                    return isMobile ? <MusicCard {...item} key={index}/> :(
                        <Col key={index}>
                            <MusicCard {...item}/>
                        </Col>
                    )
                })}
            </Row>
            }
    </div>
    );
```

Для устройств с шириной экрана меньше 600 мы будем изменять количество колонок на странице.

# Доработка React приложения по варианту

### Реализовать получение данных из mock-объектов

Доработать страницу приложения по вашему варианту. Наполнение данных осуществить через mock-объекты

### Добавить Навигационную цепочку и страницу Подробнее

Добавить страницу Подробнее для просмотра данных о вашем товаре/услуге.

Для удобной навигации добавить Навигационную цепочку `Breadcrumbs`: [Магазин](/README.md) / [Название услуги](/README.md)

### Подключение к собственному API из web-сервиса

Вернемся к нашему примеру с iTunes. Теперь нам требуется заменить наши запросы `fetch` к сервису iTunes на обращение к нашему сервису `Django` или `Golang`

## Важный момент. CORS

У вас возникнет проблема с отображением проекта React с частью, связанной с json'ом, при подключении приложения к вашему веб-сервису

Как понять, что пустой экран связан с этой ошибкой?

Нажимаем правой кнопкой мыши на любое место на странице, после чего нажимаем на кнопку **Посмотреть код**. После чего переходим во вкладку **Console**, где и ищем ошибку связанную с `CORS`-политикой. Если она есть, то просто отключаем CORS. Есть разные способы, как это сделать, но я предложу очень полезное [расширение для Googl'a](https://chrome.google.com/webstore/detail/cors-unblock/lfhmikememgdcahcdlaciloancbhjino)

[iu5-javascript]: https://github.com/iu5git/JavaScript

[vite]: https://vitejs.dev/
[vite-template-project]: https://vitejs.dev/guide/#scaffolding-your-first-vite-project

[react]: https://react.dev
[react-router]: https://reactrouter.com
[react-hooks]: https://react.dev/reference/react

[typescript]: https://www.typescriptlang.org/

[habr-react-diff-class-function-component]: https://habr.com/ru/company/ruvds/blog/444348
[habr-react-hooks]: https://habr.com/ru/company/ruvds/blog/554280
