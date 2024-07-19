import React from 'react';
import { Container } from 'react-bootstrap';

const Footer = () => {
  return (
    <footer className="footer bg-light text-dark text-center py-3">
      <Container>
        <p>
          &copy; 2024{' '}
          <a href="https://github.com/xdaruis/">Darius-Andrei Rozemberg</a> All
          rights reserved
        </p>
      </Container>
    </footer>
  );
};

export default Footer;
