import React from 'react';
import { Outlet } from 'react-router-dom';

import Footer from '../Footer.js';
import NavigationBar from '../NavigationBar.js';
import './styles.css';

const Layout = () => {
  return (
    <div className="holy-grail-flexbox">
      <NavigationBar />
      <main className="main-content">
        <Outlet />
      </main>
      <section className="left-sidebar"></section>
      <aside className="right-sidebar"></aside>
      <Footer />
    </div>
  );
};

export default Layout;
