import React from 'react';

function CustomCard({ children, width = 4, title }) {
  const columnClass = `col-sm-${width + 4} col-md-${width + 2} col-lg-${width}`;

  return (
    <div className="container mt-4 mb-2">
      <div className="row justify-content-center">
        <div className={columnClass}>
          <div className="card shadow">
            {title && (
              <div className="card-header bg-primary text-white">
                <h2 className="card-title text-center mb-0">{title}</h2>
              </div>
            )}
            <div className="card-body d-flex flex-column align-items-center">
              {children}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default CustomCard;
