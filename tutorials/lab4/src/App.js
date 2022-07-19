import { BrowserRouter, Route, Link, Switch } from "react-router-dom";
import StartPage from "./pages/StartPage/StartPage";
import ITunesPage from "./pages/ITunesPage/ITunesPage";
import { Navbar, Container, Nav, NavDropdown } from 'react-bootstrap'
function App() {

  return (
      <BrowserRouter basename="/" >
        <Navbar bg="light" expand="lg">
          <Container>
            <Navbar.Brand href="#home">Лаба 8</Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
              <Nav className="me-auto">
                <Link to="/"><span style={{margin:'0 12px'}}>Стартовая страница</span></Link>
                  <br/>
                <Link to="/new"><span style={{margin:'0 12px'}}>Хочу на страницу с чем-то новеньким(Пустая страничка)</span></Link>
                  <br/>
                <Link to="/music"><span style={{margin:'0 12px'}}>Хочу на страницу с рабочим апи ITunes</span></Link>
              </Nav>
            </Navbar.Collapse>
          </Container>
        </Navbar>
        <div>
          <Switch>
            <Route exact path="/">
             <StartPage/>
            </Route>
            <Route path="/new">
              <h1>Это наша страница с чем-то новеньким</h1>
            </Route>
            <Route path="/music">
             <ITunesPage/>
            </Route>
          </Switch>
        </div>
      </BrowserRouter>
  );
}

export default App;
