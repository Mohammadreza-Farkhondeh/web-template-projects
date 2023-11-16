import React, { useState } from 'react';
import api from '../api/Api';

const SignUp = () => {
  const [userData, setUserData] = useState({
    username: '',
    password1: '',
    password2: '',
  });

  const handleInputChange = (e) => {
    setUserData({
      ...userData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSignUp = () => {
    // validation logic here before calling signup
    try {
      const result = api.post('auth/signup/', userData)
      console.log(result)
    } catch (error) {
      console.error(error.message)
    }
  };

  return (
    <div>
      <h2>Sign Up</h2>
      <form>
        <label>
          Username:
          <input type="text" name="username" onChange={handleInputChange} />
        </label>
        <br />
        <label>
          Password:
          <input type="password" name="password1" onChange={handleInputChange} />
        </label>
        <label>
          Password again:
          <input type="password" name="password2" onChange={handleInputChange} />
        </label>
        <br />        <button type="button" onClick={handleSignUp}>
          Sign Up
        </button>
      </form>
    </div>
  );
};

export default SignUp;
