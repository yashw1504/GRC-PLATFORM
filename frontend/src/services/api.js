import axios from "axios";

const API = axios.create({
  baseURL: "http://43.205.236.141:8000"
});

export default API;