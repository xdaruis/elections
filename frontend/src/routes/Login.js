import axios from 'axios';
import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Link, useNavigate } from 'react-router-dom';

import CustomCard from '../components/CustomCard.js';
import CustomInput from '../components/CustomInput.js';
import { login } from '../features/auth.js';

const Login = () => {
  const [userData, setUserData] = useState({});
  const isAuthenticated = useSelector((state) => state.auth.isAuthenticated);
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [spam, setSpam] = useState(false);

  const submitForm = (e) => {
    e.preventDefault();
    if (isAuthenticated) {
      alert('Already logged in');
      return;
    }
    if (spam) return;
    setSpam(true);

    axios
      .post('/api/user/token/', userData, {
        headers: { 'Content-Type': 'application/json' }
      })
      .then((response) => {
        const data = response.data;
        if (data.token) {
          dispatch(login({ token: data.token, username: userData.username }));
          navigate('/', { replace: true });
        } else {
          const errorMessages = Object.values(data).flat().join('\n');
          alert(errorMessages);
        }
      })
      .catch((error) => {
        if (error.response && error.response.data) {
          const errorData = error.response.data;
          const errorMessages = Object.values(errorData)
            .flat()
            .filter((message) => typeof message === 'string')
            .join('\n');
          alert(errorMessages);
        } else if (error.request) {
          alert('No response received from server. Please try again.');
        } else {
          alert('Error: ' + error.message);
        }
      })
      .finally(() => {
        setSpam(false);
      });
  };

  return (
    <>
      <CustomCard>
        <form onSubmit={submitForm}>
          <div className="mb-md-2 mt-md-3 pb-5">
            <h2 className="fw-bold mb-5 text-uppercase">Sign in</h2>
            <div className="form-group mb-4 text-start">
              <CustomInput setData={setUserData} type="username" />
              <CustomInput setData={setUserData} type="password" />
            </div>
            <button
              className="btn btn-outline-primary btn-lg px-5"
              type="submit"
            >
              Login
            </button>
            <p className="small mt-3 pb-lg-2">
              <a className="text-50" href="#!">
                Forgot password?
              </a>
            </p>
          </div>
        </form>
        <div>
          <p className="mb-0 text-end">
            Don&apos;t have an account?{' '}
            <Link to="/register" className="text-50 fw-bold">
              Sign Up
            </Link>
          </p>
        </div>
      </CustomCard>
    </>
  );
};

export default Login;
