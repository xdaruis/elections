import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Link, useNavigate } from 'react-router-dom';

import CustomCard from '../../components/ui/CustomCard';
import CustomForm from '../../components/ui/CustomForm';
import CustomInput from '../../components/ui/CustomInput';
import { login } from '../../features/auth';
import getError from '../../utils/getError';

function Login() {
  const [error, setError] = useState('');
  const [userData, setUserData] = useState({
    username: '',
    password: ''
  });
  const isAuthenticated = useSelector((state) => state.auth.isAuthenticated);
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [isSubmitting, setIsSubmitting] = useState(false);

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
    if (!verifyUserData()) return;
    if (isSubmitting) return;

    setIsSubmitting(true);
    try {
      const { data } = await axios.post('/api/user/token/', userData, {
        headers: { 'Content-Type': 'application/json' }
      });
      if (data.token) {
        dispatch(login({ token: data.token, username: userData.username }));
        navigate('/', { replace: true });
      }
    } catch (err) {
      setError(getError(err));
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <CustomCard width={5}>
      <CustomForm
        handleSubmit={submitForm}
        error={error}
        title="SIGN IN"
        submitLabel="Login"
      >
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
      </CustomForm>
      <p className="small mt-0 pb-lg-2">
        <Link className="text-50" to="#!">
          Forgot password?
        </Link>
      </p>
      <div>
        <p className="mb-0 text-end">
          Don&apos;t have an account?{' '}
          <Link
            to="/register"
            className="text-50 fw-bold"
            disabled={isSubmitting}
          >
            Sign Up
          </Link>
        </p>
      </div>
    </CustomCard>
  );
}

export default Login;
