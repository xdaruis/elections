import axios from 'axios';
import React, { useState } from 'react';
import { useSelector } from 'react-redux';
import { Link, useNavigate } from 'react-router-dom';

import CustomCard from '../components/CustomCard';
import CustomInput from '../components/CustomInput';
import InfoText from '../components/ui/InfoText';

function Register() {
  const [error, setError] = useState('');
  const [userData, setUserData] = useState({});
  const [confirmPassword, setConfirmPassword] = useState({});
  const isAuthenticated = useSelector((state) => state.auth.isAuthenticated);
  const navigate = useNavigate();

  const submitForm = (e) => {
    e.preventDefault();
    if (isAuthenticated) {
      setError('Already logged in');
      return;
    }

    if (confirmPassword.password !== userData.password) {
      setError("Passwords don't match!");
      return;
    }

    axios
      .post('/api/user/create/', userData, {
        headers: {
          'Content-Type': 'application/json'
        }
      })
      .then((response) => {
        const { data } = response;
        if (data.email) {
          navigate('/login');
        } else {
          setError('Failed');
        }
      })
      .catch((err) => setError(err));
  };

  return (
    <CustomCard>
      <InfoText message={error} type={error} />
      <form onSubmit={submitForm}>
        <div className="mb-md-4 mt-md-3 pb-5">
          <h2 className="fw-bold mb-5 text-uppercase">Register</h2>
          <div className="form-group text-start mb-4">
            <CustomInput setData={setUserData} type="name" />
            <CustomInput setData={setUserData} type="username" />
            <CustomInput setData={setUserData} type="email" />
            <CustomInput setData={setUserData} type="password" />
            <CustomInput
              setData={setConfirmPassword}
              label="Confirm password"
              type="password"
            />
          </div>
          <button className="btn btn-outline-primary btn-lg px-5" type="submit">
            Register
          </button>
        </div>
      </form>
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
