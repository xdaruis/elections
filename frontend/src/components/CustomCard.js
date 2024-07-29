import React from 'react';

const CustomCard = ({ children }) => {
  return (
    <>
      <div className="d-flex justify-content-center">
        <div className="card border-1 w-50">
          <div className="card-body p-5 text-center">{children}</div>
        </div>
      </div>
    </>
  );
};

export default CustomCard;
