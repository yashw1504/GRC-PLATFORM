import axios from "axios";

const API = axios.create({
  baseURL: "http://13.127.79.109:8000"
});

export default API;