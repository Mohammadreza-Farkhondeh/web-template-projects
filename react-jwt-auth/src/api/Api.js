import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/',
});

// api.interceptors.request.use(
//   (config) => {
//     return config;
//   },
//   (error) => {
//     return Promise.reject(error);
//   }
// );
//
// api.interceptors.response.use(
//   (response) => {
//     return response;
//   },
//   async (error) => {
//     return Promise.reject(error);
//   }
// );

export default api;
