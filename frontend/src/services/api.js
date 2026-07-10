import axios from "axios";

const API = axios.create({
  baseURL: "http://34.228.69.213:8000"
});

export default API;