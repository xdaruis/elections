import React from 'react';
import { Container, Nav, NavDropdown, Navbar } from 'react-bootstrap';
import { PersonCircle } from 'react-bootstrap-icons';
import { useSelector , useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';

import { logout } from '../features/auth';

const NavigationBar = () => {
  const isAuthenticated = useSelector((state) => state.auth.isAuthenticated);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleLogout = (event) => {
    event.preventDefault();
    try {
      dispatch(logout());
      navigate('/login');
    } catch (error) {
      console.error('Logout failed', error);
    }
  };

  return (
    <Navbar className="header" bg="light" variant="light" expand="lg">
      <Container>
        <Navbar.Brand href="/">Elections</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link href="/">Home</Nav.Link>
            <Nav.Link href="#link">Link</Nav.Link>
          </Nav>
          <Nav>
            {isAuthenticated ? (
              <NavDropdown
                title={<PersonCircle size={24} />}
                id="user-dropdown"
                align="end"
              >
                <NavDropdown.Item href="/profile">Profile</NavDropdown.Item>
                <NavDropdown.Divider />
                <NavDropdown.Item onClick={handleLogout}>
                  Logout
                </NavDropdown.Item>
              </NavDropdown>
            ) : (
              <Nav.Link href="/login">Login</Nav.Link>
            )}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default NavigationBar;
