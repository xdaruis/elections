import React from 'react';
import { NavLink } from 'react-router-dom';

function CustomNavLink({ label, linkTo }) {
  return (
    <NavLink
      className={({ isActive }) => 'nav-link' + (isActive ? ' active' : '')}
      to={linkTo}
    >
      {label}
    </NavLink>
  );
}

export default CustomNavLink;
