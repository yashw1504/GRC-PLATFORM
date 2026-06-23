import axios from "axios";

const API = axios.create({
  baseURL: "http://13.232.166.187:8000"
});

export default API;