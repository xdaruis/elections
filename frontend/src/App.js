import axios from 'axios';
import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';

import Layout from './components/Layout/index.js';
import Loader from './components/Loader.js';
import { loaded, login, logout } from './features/auth.js';
import Home from './routes/Home.js';
import Login from './routes/Login.js';
import NotFound from './routes/NotFound.js';
import Register from './routes/Register.js';
import setAuthToken from './utils/setAuthToken.js';

if (localStorage.token) {
  setAuthToken(localStorage.token);
}

axios.defaults.withCredentials = true;

const App = () => {
  const dispatch = useDispatch();
  const isLoading = useSelector((state) => state.auth.isLoading);

  useEffect(() => {
    if (localStorage.token) {
      axios
        .get('/api/user/profile/')
        .then((response) => {
          const data = response.data;
          if (data.username) {
            dispatch(
              login({ token: localStorage.token, username: data.username })
            );
          } else {
            dispatch(logout());
          }
        })
        .catch((error) => {
          dispatch(logout());
          alert(error);
        });
    }
    dispatch(loaded());
  }, []);

  return (
    <Router>
      {isLoading && <Loader />}
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route exact path="login" element={<Login />} />
          <Route exact path="register" element={<Register />} />
        </Route>
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  );
};

export default App;
