import axios from "axios";

const API = axios.create({
  baseURL: "http://13.233.237.54:8000"
});

export default API;