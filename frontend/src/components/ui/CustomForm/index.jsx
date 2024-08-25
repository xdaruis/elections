import React from 'react';

import InfoText from '../InfoText';

function CustomForm({ handleSubmit, error, children, title, submitLabel }) {
  return (
    <form onSubmit={handleSubmit}>
      <div className="mb-md-0 mt-md-3 pb-5">
        <h2 className="fw-bold mb-5">{title}</h2>
        <InfoText message={error} type="error" />
        <div className="form-group mb-4 text-start">
          {children}
          <div className="d-flex justify-content-center mt-3 mb-0">
            <button
              className="btn btn-outline-primary btn-lg px-5"
              type="submit"
            >
              {submitLabel}
            </button>
          </div>
        </div>
      </div>
    </form>
  );
}

export default CustomForm;
