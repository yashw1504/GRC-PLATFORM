import axios from "axios";

const API = axios.create({
  baseURL: "http://13.232.51.0:8000"
});

export default API;