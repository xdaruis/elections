import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { useDispatch } from 'react-redux';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';

import { login, logout } from './features/auth';
import IsLoggedIn from './routes/IsLoggedIn';
import setAuthToken from './utils/setAuthToken';

import Layout from './components/layouts/Layout';
import Loader from './components/ui/Loader';
import Home from './pages/Home';
import Login from './pages/Login';
import NotFound from './pages/NotFound';
import Register from './pages/Register';
import Profile from './pages/user/Profile';

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
      },
      {
        path: '/user',
        element: <IsLoggedIn />,
        children: [
          {
            path: 'profile',
            element: <Profile />
          }
        ]
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
    axios.defaults.withCredentials = true;
    const setUserSession = async () => {
      if (localStorage.token) {
        setAuthToken(localStorage.token);
        try {
          const { data } = await axios.get('/api/user/profile/');
          dispatch(
            login({ token: localStorage.token, username: data.username })
          );
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
