import React from 'react';

function InfoText({ message, type }) {
  if (!message) return null;

  const messageClass = type === 'error' ? 'text-danger' : 'text-success';

  return <p className={`${messageClass} mt-1 mb-1`}>{message}</p>;
}

export default InfoText;
