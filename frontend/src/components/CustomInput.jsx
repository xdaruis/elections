import React from 'react';

function CustomInput({
  setData,
  label,
  type,
  required = false,
  id,
  className = ''
}) {
  const handleChange = (e) => {
    const { value } = e.target;
    setData((prevData) => ({
      ...prevData,
      [id]: value
    }));
  };

  return (
    <div className={`form-group mt-3 ${className}`}>
      {label && <label htmlFor={id}>{label}:</label>}
      <input
        id={id}
        type={type}
        className="form-control"
        onChange={handleChange}
        required={required || undefined}
      />
    </div>
  );
}

export default CustomInput;
