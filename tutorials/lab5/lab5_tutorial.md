# Методические указания по выполнению лабораторной работы №5

## План

1. Развертывание приложения React в GitHub Pages
2. Добавление главного меню приложения
3. Добавление менеджера состояний
    1. Redux Toolkit
    2. React Context

## 1. Развертывание приложения React в GitHub Pages

С помощью `GitHub Pages` возможно развернуть статическое приложение, например наш React проект. Но развернуть наш бекенд здесь не получится.

[Пример развертывания React](https://github.com/gitname/react-gh-pages)

#### Обратите внимание

При развертывании приложения `React` через `GitHub Pages`, ваши `AJAX` запросы будут идти по `http`, в то время как приложение будет доступно по `https`. Работать это будет только при использовании адреса `localhost` в `AJAX` запросах.

## 2. Главное меню приложения

Для создания главного меню приложения будем использовать `Navbar` из `react-bootstrap`

[Подробнее](https://react-bootstrap.github.io/components/navbar/)


```jsx
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';

function BasicExample() {
  return (
    <Navbar bg="light" expand="lg">
      <Container>
        <Navbar.Brand href="#home">React-Bootstrap</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link href="#home">Home</Nav.Link>
            <Nav.Link href="#link">Link</Nav.Link>
            <NavDropdown title="Dropdown" id="basic-nav-dropdown">
              <NavDropdown.Item href="#action/3.1">Action</NavDropdown.Item>
              <NavDropdown.Item href="#action/3.2">
                Another action
              </NavDropdown.Item>
              <NavDropdown.Item href="#action/3.3">Something</NavDropdown.Item>
              <NavDropdown.Divider />
              <NavDropdown.Item href="#action/3.4">
                Separated link
              </NavDropdown.Item>
            </NavDropdown>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default BasicExample;
```

## 3. Менеджер состояний

Менеджер состояния может быть реализован через Redux Toolkit или через набор хуков `useContext` и `useReducer`

### 3.1. Redux Toolkit

[Методические указания для Redux Toolkit](https://github.com/iu5git/web-2022/blob/main/tutorials/redux/redux_toolkit.md)

### 3.2. Хуки useContext и useReducer

Для использования разными компонентами нашего приложения одних данных (одного состояния) нам потребуется использовать хук `useContext`, а для разделения различных источников и вариантов изменений этих состояний мы будем использовать хук `useReducer`

#### useContext

[Контекст](https://reactjs.org/docs/hooks-reference.html#usecontext) разработан для передачи данных, которые можно назвать «глобальными» для всего дерева React-компонентов

#### useReducer

[Редюсер](https://reactjs.org/docs/hooks-reference.html#usereducer)


