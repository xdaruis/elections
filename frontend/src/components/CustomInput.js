import React from 'react';

const CustomInput = ({ setData, label, type }) => {
  const handleChange = (e) => {
    const { id, value } = e.target;
    setData((prevData) => ({
      ...prevData,
      [id]: value
    }));
  };

  return (
    <>
      <label className="mt-2">
        {label ? label : type.charAt(0).toUpperCase() + type.slice(1)}
      </label>
      <input
        type={type}
        className="form-control"
        required
        id={type}
        onChange={handleChange}
      />
    </>
  );
};

export default CustomInput;
