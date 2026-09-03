import axios from "axios";

const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8080";

const client = axios.create({ baseURL: BASE_URL });

client.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authApi = {
  register: (username, password) =>
    client.post("/api/auth/register", { username, password }).then((r) => r.data),
  login: (username, password) =>
    client.post("/api/auth/login", { username, password }).then((r) => r.data),
};

export const documentApi = {
  compare: (fileA, fileB) => {
    const form = new FormData();
    form.append("fileA", fileA);
    form.append("fileB", fileB);
    return client
      .post("/api/documents/compare", form, {
        headers: { "Content-Type": "multipart/form-data" },
      })
      .then((r) => r.data);
  },
  analyze: (file) => {
    const form = new FormData();
    form.append("file", file);
    return client
      .post("/api/documents/analyze", form, {
        headers: { "Content-Type": "multipart/form-data" },
      })
      .then((r) => r.data);
  },
  history: () => client.get("/api/documents/history").then((r) => r.data),
};

export default client;
