import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { useDispatch } from 'react-redux';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';

import Layout from './components/layouts/Layout';
import Loader from './components/ui/Loader';
import { login, logout } from './features/auth';
import Home from './pages/Home';
import Login from './pages/Login';
import NotFound from './pages/NotFound';
import Register from './pages/Register';
import Profile from './pages/user/Profile';
import IsLoggedIn from './routes/IsLoggedIn';
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
      },
      {
        path: '/user',
        element: <IsLoggedIn />,
        children: [
          {
            path: '/user/profile',
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
    const setUserSession = async () => {
      if (localStorage.token) {
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
