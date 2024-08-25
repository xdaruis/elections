import axios from 'axios';
import React, { useState } from 'react';
import { useSelector } from 'react-redux';
import { Link, useNavigate } from 'react-router-dom';

import CustomCard from '../../components/ui/CustomCard';
import CustomForm from '../../components/ui/CustomForm';
import CustomInput from '../../components/ui/CustomInput';
import InfoText from '../../components/ui/InfoText';

function Register() {
  const [error, setError] = useState('');
  const [userData, setUserData] = useState({});
  const [confirmPassword, setConfirmPassword] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const isAuthenticated = useSelector((state) => state.auth.isAuthenticated);
  const navigate = useNavigate();

  const submitForm = async (e) => {
    e.preventDefault();
    if (isAuthenticated) {
      setError('Already logged in');
      return;
    }

    if (confirmPassword.confirm !== userData.password) {
      setError("Passwords don't match!");
      return;
    }

    if (isSubmitting) return;
    setIsSubmitting(true);

    try {
      const { data } = await axios.post('/api/user/create/', userData, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      if (data.email) {
        navigate('/login');
      }
    } catch (err) {
      const message = err.response?.data;
      setError(
        message.error ||
          message[Object.keys(message)[0]] ||
          'An unexpected error occured'
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <CustomCard width={5}>
      <InfoText message={error} type={error} />
      <CustomForm
        handleSubmit={submitForm}
        error={error}
        title="REGISTER"
        submitLabel="Register"
      >
        <CustomInput
          label="Name"
          id="name"
          setData={setUserData}
          type="name"
          required
        />
        <CustomInput
          label="Username"
          id="username"
          setData={setUserData}
          type="username"
          required
        />
        <CustomInput
          label="Email"
          id="email"
          setData={setUserData}
          type="email"
          required
        />
        <CustomInput
          label="Password"
          id="password"
          setData={setUserData}
          type="password"
          required
        />
        <CustomInput
          id="confirm"
          setData={setConfirmPassword}
          label="Confirm password"
          type="password"
          required
        />
      </CustomForm>
      <div>
        <p className="mb-0 text-end">
          Already have an account?{' '}
          <Link to="/login" className="text-50 fw-bold">
            Login
          </Link>
        </p>
      </div>
    </CustomCard>
  );
}

export default Register;
