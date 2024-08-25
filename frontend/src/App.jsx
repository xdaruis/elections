import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { useDispatch } from 'react-redux';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';

import Layout from './components/Layout/index';
import Loader from './components/Loader';
import { login, logout } from './features/auth';
import Home from './routes/Home';
import Login from './routes/Login';
import NotFound from './routes/NotFound';
import Register from './routes/Register';
import setAuthToken from './utils/setAuthToken';

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

function App() {
  const dispatch = useDispatch();
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    const setUserSession = async () => {
      if (localStorage.token) {
        try {
          const { data } = await axios.get('/api/user/profile/');
          if (data.username) {
            login({ token: localStorage.token, username: data.username });
          } else {
            dispatch(logout());
          }
        } catch (err) {
          dispatch(logout());
        }
      }
      setLoaded(true);
    };
    setUserSession();
  }, []);

  if (!loaded) return <Loader />;

  return <RouterProvider router={router} />;
}

export default App;
