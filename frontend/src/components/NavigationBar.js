import React from 'react';
import { Container, Nav, NavDropdown, Navbar } from 'react-bootstrap';
import { PersonCircle } from 'react-bootstrap-icons';

const NavigationBar = () => {
  return (
    <Navbar className="header" bg="light" variant="light" expand="lg">
      <Container>
        <Navbar.Brand href="#home">Elections</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link href="#home">Home</Nav.Link>
            <Nav.Link href="#link">Link</Nav.Link>
          </Nav>
          <Nav>
            <NavDropdown
              title={<PersonCircle size={24} />}
              id="user-dropdown"
              align="end"
            >
              <NavDropdown.Item href="#profile">Profile</NavDropdown.Item>
              <NavDropdown.Item href="#settings">Settings</NavDropdown.Item>
              <NavDropdown.Divider />
              <NavDropdown.Item href="#logout">Logout</NavDropdown.Item>
            </NavDropdown>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default NavigationBar;
