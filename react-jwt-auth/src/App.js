import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Layout from './layouts/Layout'
import Header from './layouts/Header';
import Missing from './components/Missing';
import Login from './components/Login';
import Signup from './components/Signup';

const App = () => {
  return (
    <>
    <Header />
    <Routes>

      <Route path="/" element={<Layout />}>
        <Route path="login" element={<Login />} />
        <Route path="signup" element={<Signup />} />
      </Route>

      <Route path="*" element={<Missing />} />
    </Routes>
    </>  );
};

export default App;
