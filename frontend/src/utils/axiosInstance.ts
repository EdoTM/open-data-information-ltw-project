import axios from "axios";

const BACKEND_URL: string =
  import.meta.env.VITE_BACKEND_URL ||
  window.location.origin.replace("5173", "5000");

const axiosInstance = axios.create({
  baseURL: BACKEND_URL + "/api",
  withCredentials: true,
});

export default axiosInstance;
