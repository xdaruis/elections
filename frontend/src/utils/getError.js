const getError = (error) => {
  const message = error.response?.data;
  let finalMessage = 'An unexpected error occurred';

  if (typeof message === 'string') {
    if (!message.trim().toLowerCase().startsWith('<!doctype html>')) {
      finalMessage = message;
    }
  } else if (message && typeof message === 'object') {
    finalMessage =
      message.error ||
      message.message ||
      message[Object.keys(message)[0]] ||
      finalMessage;
  }

  return finalMessage;
};

export default getError;
