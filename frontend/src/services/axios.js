import axios from "axios";
import router from "../router";

const api = axios.create({
  baseURL: "http://127.0.0.1:8080",
});

// Request interceptor
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (
      error.response &&
      (error.response.status === 401 || error.response.status === 422)
    ) {
      // 🔒 Token expired or invalid — redirect to login
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      router.push("/login");
    }

    return Promise.reject(error);
  }
);

export default api;
