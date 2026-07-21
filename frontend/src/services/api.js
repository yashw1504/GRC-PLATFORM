import axios from "axios";

const API = axios.create({
  baseURL: "http://13.127.12.254:8000"
});

export default API;