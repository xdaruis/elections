import React from 'react';
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';

import Layout from './components/Layout/index.js';
import Home from './routes/Home.js';
import Login from './routes/Login.js';
import NotFound from './routes/NotFound.js';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route exact path="login" element={<Login />} />
        </Route>
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  );
};

export default App;
