import axios from 'axios';

// Use environment variable or default to localhost
const API_BASE = import.meta.env.VITE_API_URL || 'http://13.127.12.254:8000';

const API = axios.create({
  baseURL: API_BASE,
  timeout: 300000, // 5 min timeout for scans
});

export default API;