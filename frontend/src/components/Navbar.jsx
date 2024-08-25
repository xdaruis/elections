import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Link, NavLink, useNavigate } from 'react-router-dom';

import { logout } from '../features/auth';
import CustomDropdown from './ui/CustomDropdown/index';
import CustomNavLink from './ui/CustomNavLink';

function Navbar() {
  const isAuthenticated = useSelector((state) => state.auth.isAuthenticated);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleLogout = (e) => {
    e.preventDefault();
    try {
      dispatch(logout());
      navigate('/login');
    } catch (error) {
      // ignored
    }
  };

  const mainItems = [
    { label: 'Profile', path: '/profile' },
    { label: 'TBA', path: '/' }
  ];

  const additionalItems = [
    { label: 'Logout', onClick: handleLogout, isButton: true }
  ];

  const toggleProps = {
    className: '',
    id: 'user-dropdown',
    icon: <i className="bi bi-person-circle fs-4" />
  };

  return (
    <nav
      className="header navbar navbar-expand-sm navbar-light bg-light
        shadow-sm"
    >
      <div className="container-fluid">
        <NavLink className="navbar-brand" to="/">
          Elections
        </NavLink>
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon" />
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav me-auto mb-2 mb-lg-0">
            <li className="nav-item">
              <CustomNavLink label="Home" linkTo="/" />
            </li>
            <li className="nav-item">
              <CustomNavLink label="TBA" linkTo="/TBA" />
            </li>
          </ul>
          {isAuthenticated ? (
            <CustomDropdown
              mainItems={mainItems}
              additionalItems={additionalItems}
              toggleProps={toggleProps}
            />
          ) : (
            <Link className="nav-link" to="/login">
              Login
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
