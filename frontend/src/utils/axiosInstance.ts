import axios from "axios";

const BACKEND_URL: string =
  import.meta.env.VITE_BACKEND_URL ||
  (import.meta.env.VITE_BACKEND_SAME_PORT && window.location.origin) ||
  window.location.origin.replace("5173", "5000");

const axiosInstance = axios.create({
  baseURL: BACKEND_URL + "/api",
  withCredentials: true,
});

export default axiosInstance;
