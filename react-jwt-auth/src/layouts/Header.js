import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import {Link} from "react-router-dom";

const Header = () => {
  const { credential, loading, logout } = useAuth();

  const handleLogout = () => {
    logout();
  };

  return (
    <div>
      <h1>My App</h1>
      {loading && <p>Loading...</p>}
      {credential ? (
        <div>
          <button onClick={handleLogout}>Logout</button>
          <Link to={'/profile'}><strong>{credential.username}</strong>Profile</Link>
        </div>
      ) : (
        <div>
          <Link to={'/login'}>Login</Link>
          <Link to={'/signup'}>Signup</Link>
        </div>
      )}
    </div>
  );
};

export default Header;
