import React from 'react';
import { Link } from 'react-router-dom';

const NotFound = () => {
  return (
    <div className="d-flex flex-column justify-content-center mt-5">
      <div className="text-center">
        <h1>Oops. 404&apos;d!</h1>
        <p>The page you are looking for does not exist.</p>
        <Link to="/" className="btn btn-outline-secondary btn-lg px-5">
          Take Me Home
        </Link>
      </div>
    </div>
  );
};

export default NotFound;
