import React from 'react';
import { Link } from 'react-router-dom';

function Footer() {
  return (
    <footer className="footer bg-light text-dark text-center py-3">
      <div className="container">
        <p className="text-muted">
          &copy; 2024
          <Link to="https://github.com/xdaruis/">
            {' '}
            Darius-Andrei Rozemberg{' '}
          </Link>
          All rights reserved
        </p>
      </div>
    </footer>
  );
}

export default Footer;
