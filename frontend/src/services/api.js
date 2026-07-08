import axios from "axios";

const API = axios.create({
  baseURL: "http://3.110.88.20:8000"
});

export default API;