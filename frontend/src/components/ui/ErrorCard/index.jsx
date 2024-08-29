import React from 'react';

import './styles.css';

function ErrorCard({
  message = 'An error occurred while processing your request.'
}) {
  return (
    <div className="container mt-5">
      <div className="card error-card">
        <div className="card-body">
          <div className="d-flex align-items-center mb-3">
            <div className="error-icon me-3">&#9888;</div>
            <h5 className="error-title mb-0">Error</h5>
          </div>
          <p className="error-message mb-0">{message}</p>
        </div>
      </div>
    </div>
  );
}
export default ErrorCard;
