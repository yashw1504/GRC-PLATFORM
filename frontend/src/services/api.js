import axios from 'axios';

// Use a placeholder that gets replaced at container runtime
const API_BASE = '__API_URL__' || '/api';

const API = axios.create({
  baseURL: API_BASE,
  timeout: 300000,
});

export default API;