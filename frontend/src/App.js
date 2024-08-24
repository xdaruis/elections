import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { useDispatch } from 'react-redux';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';

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

const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      {
        path: '/',
        element: <Home />
      },
      {
        path: '/login',
        element: <Login />
      },
      {
        path: '/register',
        element: <Register />
      }
    ]
  },
  {
    path: '*',
    element: <NotFound />
  }
]);

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

  return <RouterProvider router={router} />;
};

export default App;
