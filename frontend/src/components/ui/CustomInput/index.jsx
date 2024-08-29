import React from 'react';

function CustomInput({
  setData,
  label,
  type,
  required = false,
  id,
  className = '',
  value = false
}) {
  const handleChange = (e) => {
    setData((prevData) => ({
      ...prevData,
      [id]: e.target.value
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
        value={value || undefined}
      />
    </div>
  );
}

export default CustomInput;
