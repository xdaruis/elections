import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Link, useNavigate } from 'react-router-dom';

import CustomCard from '../components/ui/CustomCard';
import CustomInput from '../components/ui/CustomInput';
import InfoText from '../components/ui/InfoText';
import { login } from '../features/auth';

function Login() {
  const [error, setError] = useState('');
  const [userData, setUserData] = useState({
    username: '',
    password: ''
  });
  const isAuthenticated = useSelector((state) => state.auth.isAuthenticated);
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [isSpam, setIsSpam] = useState(false);

  useEffect(() => {
    setError('');
  }, [userData]);

  const verifyUserData = () => {
    if (!userData.username) {
      setError('Username field required');
      return false;
    }
    if (!userData.password) {
      setError('Password field required');
      return false;
    }
    return true;
  };

  const submitForm = async (e) => {
    e.preventDefault();
    if (isAuthenticated) {
      setError('Already logged in');
      return;
    }
    if (isSpam) return;
    if (!verifyUserData()) return;

    setIsSpam(true);
    try {
      const { data } = await axios.post('/api/user/token/', userData, {
        headers: { 'Content-Type': 'application/json' }
      });
      if (data.token) {
        dispatch(login({ token: data.token, username: userData.username }));
        navigate('/', { replace: true });
      }
    } catch (err) {
      const message = err.response?.data;
      setError(
        message.error ||
          message[Object.keys(message)[0]] ||
          'An unexpected error occured'
      );
    } finally {
      setIsSpam(false);
    }
  };

  return (
    <CustomCard width={5}>
      <form onSubmit={submitForm}>
        <div className="mb-md-2 mt-md-3 pb-5">
          <h2 className="fw-bold mb-5 text-uppercase">Sign in</h2>
          <InfoText message={error} type="error" />
          <div className="form-group mb-4 text-start">
            <CustomInput
              id="username"
              label="Username"
              setData={setUserData}
              type="username"
              required
            />
            <CustomInput
              id="password"
              label="Password"
              setData={setUserData}
              type="password"
              required
            />
          </div>
          <div className="d-flex flex-column align-items-center">
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
        </div>
      </form>
      <div>
        <p className="mb-0 text-end">
          Don&apos;t have an account?{' '}
          <Link to="/register" className="text-50 fw-bold" disabled={isSpam}>
            Sign Up
          </Link>
        </p>
      </div>
    </CustomCard>
  );
}

export default Login;
