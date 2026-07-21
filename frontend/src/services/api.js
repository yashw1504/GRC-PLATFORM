import axios from 'axios';

// Use Vite build-time env var, fall back to nginx proxy path
const API_BASE = import.meta.env.VITE_API_URL || '/api';

const API = axios.create({
  baseURL: API_BASE,
  timeout: 300000,
});

export default API;