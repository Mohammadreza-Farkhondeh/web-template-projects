import React, { createContext, useContext, useState, useEffect } from 'react';
import { jwtDecode } from "jwt-decode";
import api from '../api/Api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [credential, setCredential] = useState(getCredentialFromLocalStorage());
  const [loading, setLoading] = useState(false);

  function getCredentialFromLocalStorage() {
    const storedCredential = localStorage.getItem('credential');
    return storedCredential ? JSON.parse(storedCredential) : null;
  }

  const refreshAccessToken = async () => {
    try {
      const refreshToken = credential.refreshToken;

      if (!refreshToken) {
        throw new Error('No refresh token available');
      }

      const response = await api.post('token/refresh/', {
        refreshToken,
      });

      const { accessToken } = response.data;
      const { exp} = jwtDecode(accessToken)

      const updatedCredential = {
        ...credential,
        accessToken,
        exp,
      };

      localStorage.setItem('credential', JSON.stringify(updatedCredential));
      setCredential(updatedCredential);

      return accessToken;
    } catch (error) {
      console.error('Refresh token failed:', error.message);
      throw error;
    }
  };

  const login = async (credentials) => {
    setLoading(true);
    try {
      const response = await api.post('auth/token/obtain/', credentials);

      const { accessToken, refreshToken } = response.data;
      const { username, exp} = jwtDecode(accessToken)

      const credential = {
        accessToken,
        refreshToken,
        exp,
        username,
      };

      localStorage.setItem('credential', JSON.stringify(credential));
      setCredential(credential);
    } catch (error) {
      console.error('Login failed:', error.message);
    } finally {
      setLoading(false);
    }
  };

  const logout = async (credential) => {
      setLoading(true);
      try{
      // await api.post('token/logout', credential);
      localStorage.removeItem('credential');
      setCredential(null);
      } catch (error) {
        console.log('Logout failed: ', error.message)
      }
      setLoading(false);
  };

  useEffect(() => {
    const checkTokenExpiration = () => {
      if (credential && credential.expiration && credential.expiration < Date.now()) {
        refreshAccessToken().catch(() => {
          logout(credential);
        });
      }
    };

    const tokenCheckInterval = setInterval(checkTokenExpiration, 60000); // Check every minute

    return () => clearInterval(tokenCheckInterval);
  }, [credential, logout, refreshAccessToken]);

  return (
    <AuthContext.Provider value={{ credential, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
