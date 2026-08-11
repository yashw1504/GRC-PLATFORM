import axios from "axios";

const API = axios.create({
  // Browser requests stay on the same origin; nginx forwards /api to backend.
  baseURL: import.meta.env.VITE_API_URL || "/api",
  timeout: 600000,
});

export default API;
