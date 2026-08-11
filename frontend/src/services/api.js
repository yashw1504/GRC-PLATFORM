import axios from "axios";

const API = axios.create({
  baseURL: "http://35.154.254.39:8000"
});

export default API;