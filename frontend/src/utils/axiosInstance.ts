import axios from "axios";

const axiosInstance = axios.create({
  baseURL: window.location.origin.replace("5173", "5000"),
  withCredentials: true,
});

export default axiosInstance;
