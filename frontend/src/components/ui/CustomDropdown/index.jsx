import React from 'react';
import { Link } from 'react-router-dom';

import './styles.css';

function CustomDropdown({ mainItems, additionalItems = [], toggleProps }) {
  return (
    <div className="dropdown">
      <button
        className={`btn btn-link dropdown-toggle bg-transparent
          border-0 p-0 ${toggleProps.className}`}
        id={toggleProps.id || 'user-dropdown'}
        data-bs-toggle="dropdown"
        aria-expanded="false"
      >
        {toggleProps.icon}
      </button>
      <ul
        className="dropdown-menu dropdown-menu-end"
        aria-labelledby={toggleProps.id || 'user-dropdown'}
      >
        {mainItems.map((item, index) => (
          <li key={index}>
            <Link
              className="dropdown-item"
              to={item.path}
              onClick={item.onClick}
            >
              {item.label}
            </Link>
          </li>
        ))}
        <li>
          <hr className="dropdown-divider" />
        </li>
        {additionalItems.map((item, index) => (
          <li key={index}>
            {item.isButton ? (
              <button className="dropdown-item" onClick={item.onClick}>
                {item.label}
              </button>
            ) : (
              <Link className="dropdown-item" to={item.path}>
                {item.label}
              </Link>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default CustomDropdown;
