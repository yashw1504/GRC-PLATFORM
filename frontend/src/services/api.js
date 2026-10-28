import axios from "axios";

const API = axios.create({
  baseURL: "http://13.235.91.131:8000"
});

export default API;