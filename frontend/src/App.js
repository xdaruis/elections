import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { useDispatch } from 'react-redux';
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';

import Layout from './components/Layout/index.js';
import Loader from './components/Loader.js';
import { login, logout } from './features/auth.js';
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
  const [loaded, setLoaded] = useState(false);
  useEffect(() => {
    const setUserSession = async () => {
      if (localStorage.token) {
        await axios
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
      setLoaded(true);
    };
    setUserSession();
  }, []);

  if (!loaded) return <Loader />;
  return (
    <Router>
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
