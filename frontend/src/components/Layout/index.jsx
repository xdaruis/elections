import React from 'react';
import { Outlet } from 'react-router-dom';

import Footer from '../Footer';
import Navbar from '../Navbar';
import './styles.css';

function Layout() {
  return (
    <div className="holy-grail-flexbox">
      <Navbar />
      <main className="main-content">
        <Outlet />
      </main>
      <section className="left-sidebar" />
      <aside className="right-sidebar" />
      <Footer />
    </div>
  );
}

export default Layout;
