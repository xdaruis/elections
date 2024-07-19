import React from 'react';

const Loader = () => {
  return (
    <div
      className="vh-100 vw-100 position-fixed top-0
        start-0 d-flex justify-content-center align-items-center
        bg-dark bg-opacity-50"
      style={{ zIndex: 9999 }}
    >
      <div
        className="spinner-border text-light"
        role="status"
        style={{ width: '3rem', height: '3rem' }}
      >
        <span className="visually-hidden">Loading...</span>
      </div>
    </div>
  );
};

export default Loader;
